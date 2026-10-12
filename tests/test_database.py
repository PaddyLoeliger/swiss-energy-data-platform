import os
from datetime import date
from decimal import Decimal

import psycopg
import pytest

from energy_platform.pipeline import DDL, Observation, load, verify

pytestmark = [pytest.mark.integration, pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="Set RUN_INTEGRATION=1 against a dedicated test database")]


@pytest.fixture(autouse=True)
def isolated_database():
    # Refuse to truncate a normal application database.
    with psycopg.connect() as conn:
        assert conn.execute("SELECT current_database()").fetchone()[0].endswith("_test")
        conn.execute(DDL)
        conn.execute("TRUNCATE electricity_production, ingestion_runs RESTART IDENTITY CASCADE")


def test_replay_and_source_correction():
    row = Observation(date(2025, 1, 1), "Wind", Decimal("1.2"))
    load([row], "a" * 64, "fixture")
    load([row], "a" * 64, "fixture")
    load([Observation(row.day, row.carrier, Decimal("1.3"))], "b" * 64, "fixture")
    assert verify()["rows"] == 1
    with psycopg.connect() as conn:
        assert conn.execute("SELECT production_gwh FROM electricity_production").fetchone()[0] == Decimal("1.3")
        assert conn.execute("SELECT count(*) FROM ingestion_runs").fetchone()[0] == 3


def test_transaction_rolls_back_on_bad_row():
    with pytest.raises(psycopg.errors.CheckViolation):
        load([Observation(date(2025, 1, 1), "Wind", Decimal("1")), Observation(date(2025, 1, 2), "Wind", Decimal("NaN"))], "a" * 64, "fixture")
    with psycopg.connect() as conn:
        assert conn.execute("SELECT count(*) FROM electricity_production").fetchone()[0] == 0
        assert conn.execute("SELECT count(*) FROM ingestion_runs").fetchone()[0] == 0


def test_negative_source_values_flagged():
    load([Observation(date(2026, 6, 14), "Speicherkraft", Decimal("-1.5"))], "a" * 64, "fixture")
    assert verify()["negative_values_flagged"] == 1
    with psycopg.connect() as conn:
        assert conn.execute("SELECT quality_flag FROM electricity_production").fetchone()[0] == "negative_source_value_review"
