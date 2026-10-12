"""Small full-snapshot pipeline: validate first, then atomically upsert."""
import csv
import hashlib
import io
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

import psycopg

SOURCE_URL = "https://www.uvek-gis.admin.ch/BFE/ogd/104/ogd104_stromproduktion_swissgrid.csv"
REQUIRED = {"Datum", "Energietraeger", "Produktion_GWh"}


@dataclass(frozen=True)
class Observation:
    day: date
    carrier: str
    gwh: Decimal


def parse_csv(payload: bytes) -> list[Observation]:
    reader = csv.DictReader(io.StringIO(payload.decode("utf-8-sig")))
    if not REQUIRED.issubset(reader.fieldnames or []):
        raise ValueError("Source schema missing required columns")
    result = []
    keys = set()
    for line, row in enumerate(reader, 2):
        try:
            day = date.fromisoformat(row["Datum"])
            carrier = row["Energietraeger"].strip()
            value = Decimal(row["Produktion_GWh"])
            if not carrier or not value.is_finite():
                raise ValueError("Empty carrier or invalid production")
            key = (day, carrier)
            if key in keys:
                raise ValueError("Duplicate date/carrier")
            keys.add(key)
            result.append(Observation(day, carrier, value))
        except (ValueError, InvalidOperation, TypeError, AttributeError) as exc:
            raise ValueError(f"Invalid source record at line {line}: {exc}") from exc
    if not result:
        raise ValueError("Source contains no observations")
    return result


def download(url: str = SOURCE_URL, attempts: int = 3) -> bytes:
    if attempts < 1:
        raise ValueError("attempts must be positive")
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "swiss-energy-data-platform/0.1"})
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = response.read(20_000_001)
            if len(payload) > 20_000_000:
                raise ValueError("Source exceeds 20 MB limit")
            return payload
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt == attempts - 1:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("Unreachable")


DDL = """
CREATE TABLE IF NOT EXISTS ingestion_runs (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    loaded_at timestamptz NOT NULL DEFAULT now(),
    source_url text NOT NULL,
    sha256 text NOT NULL CHECK (length(sha256) = 64),
    row_count integer NOT NULL CHECK (row_count > 0)
);
CREATE TABLE IF NOT EXISTS electricity_production (
    production_date date NOT NULL,
    energy_carrier text NOT NULL CHECK (length(energy_carrier) > 0),
    production_gwh numeric NOT NULL CHECK (
        production_gwh NOT IN ('NaN'::numeric, 'Infinity'::numeric, '-Infinity'::numeric)
    ),
    run_id bigint NOT NULL REFERENCES ingestion_runs(id),
    quality_flag text GENERATED ALWAYS AS
        (CASE WHEN production_gwh < 0 THEN 'negative_source_value_review' ELSE 'not_flagged' END) STORED,
    PRIMARY KEY (production_date, energy_carrier)
);
"""


def load(rows: list[Observation], sha256: str, source_url: str) -> int:
    # libpq reads PGHOST/PGUSER/PGPASSWORD etc. Credentials never enter logs.
    with psycopg.connect(connect_timeout=10) as conn:
        conn.execute(DDL)
        run_id = conn.execute(
            "INSERT INTO ingestion_runs(source_url, sha256, row_count) VALUES (%s,%s,%s) RETURNING id",
            (source_url, sha256, len(rows)),
        ).fetchone()[0]
        with conn.cursor() as cursor:
            cursor.executemany(
                """INSERT INTO electricity_production (production_date, energy_carrier, production_gwh, run_id) VALUES (%s,%s,%s,%s)
                ON CONFLICT (production_date, energy_carrier) DO UPDATE SET
                production_gwh = EXCLUDED.production_gwh, run_id = EXCLUDED.run_id""",
                [(r.day, r.carrier, r.gwh, run_id) for r in rows],
            )
    return run_id


def ingest(raw_dir: Path) -> dict:
    payload = download()
    digest = hashlib.sha256(payload).hexdigest()
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / f"{digest}.csv"
    # Content-addressed exclusive creation; concurrent runs cannot truncate it.
    try:
        with target.open("xb") as handle:
            handle.write(payload)
    except FileExistsError:
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError("Existing raw snapshot is corrupted")
    rows = parse_csv(payload)
    run_id = load(rows, digest, SOURCE_URL)
    return {"event": "ingestion_complete", "run_id": run_id, "rows": len(rows),
            "sha256": digest, "first_date": str(min(r.day for r in rows)),
            "last_date": str(max(r.day for r in rows)), "source_url": SOURCE_URL,
            "negative_values_flagged": sum(r.gwh < 0 for r in rows)}


def verify() -> dict:
    with psycopg.connect(connect_timeout=10) as conn:
        count, earliest, latest, carriers, flagged = conn.execute(
            "SELECT count(*), min(production_date), max(production_date), count(DISTINCT energy_carrier), count(*) FILTER (WHERE production_gwh < 0) FROM electricity_production"
        ).fetchone()
        run = conn.execute("SELECT id, row_count FROM ingestion_runs ORDER BY id DESC LIMIT 1").fetchone()
        linked = conn.execute("SELECT count(*) FROM electricity_production WHERE run_id = %s", (run[0],)).fetchone()[0] if run else 0
    if not count or not run or linked != run[1]:
        raise ValueError("Verification failed: latest run row count does not match stored observations")
    return {"event": "verification_passed", "rows": count, "carriers": carriers,
            "first_date": str(earliest), "last_date": str(latest), "latest_run_rows": linked,
            "negative_values_flagged": flagged, "source_age_days": (date.today() - latest).days}
