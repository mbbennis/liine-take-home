from app.index import MINUTES_PER_DAY, build_index, minute_of_week
from app.models import Day, Interval, Restaurant


def _names_at(table, day: Day, hour: int, minute: int = 0):
    return table[day.value * MINUTES_PER_DAY + hour * 60 + minute]


def test_index_half_open_boundaries():
    r = Restaurant(name="A", intervals=[Interval(Day.Mon, 11 * 60, 22 * 60)])
    table = build_index([r])
    assert "A" in _names_at(table, Day.Mon, 11, 0)  # open at exactly open time
    assert "A" in _names_at(table, Day.Mon, 21, 59)  # open one minute before close
    assert "A" not in _names_at(table, Day.Mon, 22, 0)  # closed at exact close time
    assert "A" not in _names_at(table, Day.Mon, 10, 59)  # closed one minute before open


def test_index_overnight_wraps_to_next_day():
    r = Restaurant(
        name="B", intervals=[Interval(Day.Sun, 17 * 60, 90)]
    )  # 5pm Sun - 1:30am Mon
    table = build_index([r])
    assert "B" in _names_at(table, Day.Sun, 23, 0)
    assert "B" in _names_at(table, Day.Mon, 1, 29)
    assert "B" not in _names_at(table, Day.Mon, 1, 30)
    assert "B" not in _names_at(table, Day.Sun, 16, 59)


def test_index_close_at_midnight():
    r = Restaurant(
        name="C", intervals=[Interval(Day.Tue, 11 * 60, 0)]
    )  # 11 am - 12 am (midnight)
    table = build_index([r])
    assert "C" in _names_at(table, Day.Tue, 23, 59)
    assert "C" not in _names_at(table, Day.Wed, 0, 0)
