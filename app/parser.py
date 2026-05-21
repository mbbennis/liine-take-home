import csv
from pathlib import Path

from .models import Day, Interval, Restaurant

_DAY_TOKENS = {
    "Mon": Day.Mon,
    "Tues": Day.Tue,
    "Wed": Day.Wed,
    "Thu": Day.Thu,
    "Fri": Day.Fri,
    "Sat": Day.Sat,
    "Sun": Day.Sun,
}


def _parse_time(s: str) -> int:
    """Return minute-of-day for strings like '11 am', '11:00 am', '12 pm'."""
    timepart, period = s.strip().lower().split()
    if period not in ("am", "pm"):
        raise ValueError(f"expected 'am' or 'pm', got: {period!r}")
    hour_str, _, minute_str = timepart.partition(":")
    hour = int(hour_str)
    minute = int(minute_str) if minute_str else 0
    if hour == 12:
        hour = 0
    if period == "pm":
        hour += 12
    return hour * 60 + minute


def _parse_day_group(s: str) -> list[Day]:
    """Parse 'Mon-Fri, Sat' / 'Mon, Wed-Sun' into the listed Day values."""
    days: list[Day] = []
    for part in (p.strip() for p in s.split(",")):
        if "-" in part:
            start_tok, end_tok = (p.strip() for p in part.split("-", 1))
            start = _DAY_TOKENS[start_tok].value
            end = _DAY_TOKENS[end_tok].value
            days.extend(Day(i) for i in range(start, end + 1))
        else:
            days.append(_DAY_TOKENS[part])
    return days


def _parse_hours(s: str) -> list[Interval]:
    """Parse a full Hours field like 'Mon-Fri 11 am - 10 pm / Sat 5 pm - 11 pm'."""
    intervals: list[Interval] = []
    for chunk in s.split("/"):
        tokens = chunk.split()
        if len(tokens) < 6 or tokens[-3] != "-":
            raise ValueError(f"unparseable hours chunk: {chunk!r}")
        *day_tokens, open_digits, open_period, _dash, close_digits, close_period = (
            tokens
        )
        days = _parse_day_group(" ".join(day_tokens))
        open_minute = _parse_time(f"{open_digits} {open_period}")
        close_minute = _parse_time(f"{close_digits} {close_period}")
        for day in days:
            intervals.append(
                Interval(day=day, open_minute=open_minute, close_minute=close_minute)
            )
    return intervals


def load_restaurants(csv_path: str | Path) -> list[Restaurant]:
    restaurants: list[Restaurant] = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["Restaurant Name"].strip()
            hours = row["Hours"].strip()
            restaurants.append(Restaurant(name=name, intervals=_parse_hours(hours)))
    return restaurants
