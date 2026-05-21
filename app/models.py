from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Day(Enum):
    Mon = 0
    Tue = 1
    Wed = 2
    Thu = 3
    Fri = 4
    Sat = 5
    Sun = 6

    @classmethod
    def from_datetime(cls, dt: datetime) -> "Day":
        return cls(dt.weekday())


@dataclass
class Interval:
    day: Day
    open_minute: int
    close_minute: int


@dataclass
class Restaurant:
    name: str
    intervals: list[Interval] = field(default_factory=list)
