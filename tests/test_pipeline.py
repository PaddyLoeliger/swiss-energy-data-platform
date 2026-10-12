from datetime import date
from decimal import Decimal
from unittest.mock import patch
import urllib.error

import pytest

from energy_platform.pipeline import download, parse_csv

HEADER = "Datum,Energietraeger,Produktion_GWh\n"


def test_bom_decimal_and_extra_column():
    row = parse_csv(b"\xef\xbb\xbfDatum,Energietraeger,Produktion_GWh,extra\n2025-01-01,Wind,0.1,ignored\n")[0]
    assert (row.day, row.carrier, row.gwh) == (date(2025, 1, 1), "Wind", Decimal("0.1"))


def test_negative_source_value_preserved():
    assert parse_csv((HEADER + "2026-06-14,Speicherkraft,-1.5\n").encode())[0].gwh == Decimal("-1.5")


@pytest.mark.parametrize("body", ["", "2025-02-30,Wind,1\n", "2025-01-01,,1\n", "2025-01-01,Wind,NaN\n", "2025-01-01,Wind,Infinity\n", "2025-01-01,Wind,\n", "2025-01-01,Wind,1\n2025-01-01,Wind,2\n"])
def test_invalid_records_rejected(body):
    with pytest.raises(ValueError):
        parse_csv((HEADER + body).encode())


def test_schema_drift():
    with pytest.raises(ValueError, match="schema"):
        parse_csv(b"date,value\n2025-01-01,1\n")


def test_retry_exhaustion():
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("offline")) as request, patch("time.sleep"):
        with pytest.raises(urllib.error.URLError):
            download()
        assert request.call_count == 3


def test_retry_recovers():
    from unittest.mock import MagicMock
    response = MagicMock()
    response.__enter__.return_value.read.return_value = b"data"
    with patch("urllib.request.urlopen", side_effect=[TimeoutError(), response]), patch("time.sleep"):
        assert download() == b"data"
