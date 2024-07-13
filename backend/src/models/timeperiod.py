from __future__ import annotations
from dataclasses import dataclass
from datetime import timedelta, datetime, timezone

from models.settlement import TimePeriodId

frequency = timedelta(minutes=15)
genesis = datetime(2024, 6, 7, 22, 0, tzinfo=timezone.utc)


@dataclass(frozen=True)
class TimePeriod:

    start: datetime
    end: datetime

    @staticmethod
    def from_datetime(start: datetime) -> TimePeriod:
        return TimePeriod(start, start+frequency)

    @staticmethod
    def from_id(id: TimePeriodId) -> TimePeriod:
        start = genesis + frequency * id
        return TimePeriod(start, start+frequency)

