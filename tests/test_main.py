import datetime
import pytest
import main

def test_parseDate_valid():
    assert main.parseDate('041126') == datetime.date(2026,11,4)

def test_parseDate_invalid():
    with pytest.raises(ValueError):
        main.parseDate('311399')

def test_parseTime_valid():
    assert main.parseTime('2311')

def test_parseTime_invalid():
    with pytest.raises(ValueError):
        main.parseTime('2411')