"""Exercise real dbt models against isolated PostgreSQL; no public network."""
import os
import subprocess
from datetime import date, timedelta
from decimal import Decimal

import psycopg
import pytest
from energy_platform.pipeline import DDL, Observation, load

pytestmark = [pytest.mark.integration, pytest.mark.skipif(os.getenv("RUN_DBT_INTEGRATION") != "1", reason="Run through analytics-tests service")]
CARRIERS = ["Flusskraft", "Kernkraft", "Photovoltaik", "Speicherkraft", "Thermische", "Wind"]
START = date(2025, 1, 1)


def dbt(*args, success=True):
    result = subprocess.run(["dbt", *args], text=True, capture_output=True, timeout=180)
    if success:
        assert result.returncode == 0, result.stdout + result.stderr
    return result


def fetch(sql):
    with psycopg.connect() as conn:
        return conn.execute(sql).fetchall()


@pytest.fixture(autouse=True)
def isolated_database():
    with psycopg.connect() as conn:
        assert conn.execute("select current_database()").fetchone()[0].endswith("_test")
        conn.execute(DDL)
        conn.execute("TRUNCATE electricity_production, ingestion_runs RESTART IDENTITY CASCADE")


def observations():
    return [Observation(START + timedelta(days=day), carrier, Decimal("10")) for day in range(10) for carrier in CARRIERS]


def test_dbt_corrections_replay_and_calendar_quality():
    original = observations()
    load(original, "a" * 64, "fixture")
    dbt("build")
    assert fetch("select usable_total_gwh from analytics.fct_daily_generation where production_date = '2025-01-01'")[0][0] == 60
    assert fetch("select average_daily_gwh_7d from analytics.fct_generation_rolling where production_date = '2025-01-07'")[0][0] == 60
    assert fetch("select average_daily_gwh_7d from analytics.fct_generation_rolling where production_date = '2025-01-06'")[0][0] is None

    # Correct a historical day. Replaying it twice must not create duplicates.
    corrected = [Observation(START, "Wind", Decimal("17"))]
    load(corrected, "b" * 64, "fixture")
    load(corrected, "b" * 64, "fixture")
    dbt("build")
    assert fetch("select count(*) from analytics.fct_daily_generation_mix")[0][0] == 60
    assert fetch("select usable_total_gwh from analytics.fct_daily_generation where production_date = '2025-01-01'")[0][0] == 67
    assert fetch("select average_daily_gwh_7d from analytics.fct_generation_rolling where production_date = '2025-01-07'")[0][0] == 61
    assert fetch("select average_daily_gwh_7d from analytics.fct_generation_rolling where production_date = '2025-01-08'")[0][0] == 60
    share = fetch("select generation_share from analytics.fct_daily_generation_mix where production_date = '2025-01-01' and energy_carrier = 'Wind'")[0][0]
    assert abs(share - Decimal(17) / 67) < Decimal("0.000000001")

    # A fully missing day, a partial day, a negative value, and a zero-total day.
    with psycopg.connect() as conn:
        conn.execute("DELETE FROM electricity_production WHERE production_date = '2025-01-03' OR (production_date = '2025-01-04' AND energy_carrier = 'Wind')")
    load([Observation(START + timedelta(days=4), "Wind", Decimal("-1"))] + [Observation(START + timedelta(days=5), c, Decimal(0)) for c in CARRIERS], "c" * 64, "fixture")
    dbt("build")
    assert fetch("select count(*) from analytics.fct_daily_generation")[0][0] == 10
    assert fetch("select reported_total_gwh, is_complete_day from analytics.fct_daily_generation where production_date = '2025-01-03'")[0] == (None, False)
    assert fetch("select is_complete_day from analytics.fct_daily_generation where production_date = '2025-01-04'")[0][0] is False
    assert fetch("select production_gwh, generation_share from analytics.fct_daily_generation_mix where production_date = '2025-01-05' and energy_carrier = 'Wind'")[0] == (Decimal(-1), None)
    assert fetch("select usable_total_gwh from analytics.fct_daily_generation where production_date = '2025-01-06'")[0][0] == 0
    assert fetch("select count(generation_share) from analytics.fct_daily_generation_mix where production_date between '2025-01-03' and '2025-01-06'")[0][0] == 0
    assert fetch("select average_daily_gwh_7d from analytics.fct_generation_rolling where production_date = '2025-01-10'")[0][0] is None

    # Unknown categories must fail the contract instead of disappearing silently.
    load([Observation(START, "Unreviewed category", Decimal(1))], "d" * 64, "fixture")
    failure = dbt("test", "--select", "stg_electricity_production", success=False)
    assert failure.returncode == 1, failure.stdout + failure.stderr
    assert "relationships" in failure.stdout
