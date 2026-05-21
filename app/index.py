from datetime import datetime

from .models import Restaurant

MINUTES_PER_DAY = 24 * 60
MINUTES_PER_WEEK = 7 * MINUTES_PER_DAY


def minute_of_week(dt: datetime) -> int:
    return dt.weekday() * MINUTES_PER_DAY + dt.hour * 60 + dt.minute


def build_index(restaurants: list[Restaurant]) -> list[list[str]]:
    """Precompute a lookup table mapping minute-of-week to open restaurant names.

    Intervals where close <= open wrap into the following day's slots.
    Semantics are half-open: a restaurant is open at minute t iff open <= t < close.
    """
    table: list[list[str]] = [[] for _ in range(MINUTES_PER_WEEK)]
    for restaurant in restaurants:
        for interval in restaurant.intervals:
            start = interval.day.value * MINUTES_PER_DAY + interval.open_minute
            if interval.close_minute > interval.open_minute:
                end = interval.day.value * MINUTES_PER_DAY + interval.close_minute
            else:
                end = interval.day.value * MINUTES_PER_DAY + MINUTES_PER_DAY + interval.close_minute
            for slot in range(start, end):
                table[slot % MINUTES_PER_WEEK].append(restaurant.name)
    return table
