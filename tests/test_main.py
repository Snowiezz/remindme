import datetime
import pytest
import main

def test_parseDate_valid():
    assert main.parseDate('041126') == datetime.date(2026,11,4)

def test_parseDate_invalid():
    with pytest.raises(ValueError):
        main.parseDate('311399')

def test_parseTime_valid():
    assert main.parseTime('2311') == '2311'

def test_parseTime_invalid():
    with pytest.raises(ValueError):
        main.parseTime('2411')

#setup code
@pytest.fixture(autouse=True)
def tempDate(tmp_path,monkeypatch): # returns eventpath back to normal after
    monkeypatch.setattr(main, 'EVENTS_FILE', tmp_path / 'events.json')
    monkeypatch.setattr(main, 'DELETED_FILE', tmp_path / 'deleted_events.json')
    monkeypatch.setattr(main, 'events', {})
    monkeypatch.setattr(main, 'pendingDeletes', [])
    monkeypatch.setattr(main, 'eventNum', 1)

def test_addEvent_storesEvent():
    main.addEvent('Essay due', datetime.date(2026,11,4),'0900','CS101', None)

    assert main.events[1]['desc'] == 'Essay due'
    assert main.events[1]['type'] == 'O'

def test_addEvent_recurring():
    main.addEvent('Lecture notes to be completed',datetime.date(2026,10,25),'0800',11121,'WEEKLY')

    assert main.events[1]['type'] == 'R'
    assert main.events[1]['freq'] == 'WEEKLY'


