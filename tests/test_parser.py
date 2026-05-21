from app.models import Day
from app.parser import _parse_day_group, _parse_hours, _parse_time


def test_parse_time_basic():
    assert _parse_time("11 am") == 11 * 60
    assert _parse_time("11:00 am") == 11 * 60
    assert _parse_time("11:30 pm") == 23 * 60 + 30


def test_parse_time_midnight_and_noon():
    assert _parse_time("12 am") == 0
    assert _parse_time("12 pm") == 12 * 60


def test_parse_day_group_range():
    assert _parse_day_group("Mon-Fri") == [Day.Mon, Day.Tue, Day.Wed, Day.Thu, Day.Fri]


def test_parse_day_group_mixed():
    # 'Mon, Wed-Sun' means Tuesday is closed
    assert _parse_day_group("Mon, Wed-Sun") == [
        Day.Mon,
        Day.Wed,
        Day.Thu,
        Day.Fri,
        Day.Sat,
        Day.Sun,
    ]


def test_parse_day_group_tues_alias():
    assert _parse_day_group("Tues-Fri") == [Day.Tue, Day.Wed, Day.Thu, Day.Fri]


def test_parse_hours_multiple_ranges():
    intervals = _parse_hours("Mon-Thu 11 am - 10 pm  / Fri-Sat 11 am - 11 pm")
    days_open = {(i.day, i.open_minute, i.close_minute) for i in intervals}
    assert (Day.Mon, 11 * 60, 22 * 60) in days_open
    assert (Day.Fri, 11 * 60, 23 * 60) in days_open
    assert (Day.Sat, 11 * 60, 23 * 60) in days_open
    assert not any(i.day == Day.Sun for i in intervals)


def test_parse_hours_overnight():
    # close < open indicates wrap into next day
    intervals = _parse_hours("Mon-Sun 5 pm - 1:30 am")
    for i in intervals:
        assert i.open_minute == 17 * 60
        assert i.close_minute == 90
