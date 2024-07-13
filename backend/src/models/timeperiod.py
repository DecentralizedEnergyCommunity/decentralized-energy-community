from __future__ import annotations
from dataclasses import dataclass
from datetime import timedelta, datetime, timezone

TimePeriodId = int

frequency = timedelta(minutes=15)
genesis = datetime(2024, 6, 7, 22, 0, tzinfo=timezone.utc)


@dataclass(frozen=True)
class TimePeriod:

    start: datetime
    end: datetime

    @property
    def end_exclusive(self):
        return self.end - timedelta(minutes=15)

    @staticmethod
    def quarter_hour(start: datetime) -> TimePeriod:
        return TimePeriod(start, start+frequency)

    @staticmethod
    def from_id(id: TimePeriodId) -> TimePeriod:
        start = genesis + frequency * id
        return TimePeriod(start, start+frequency)

