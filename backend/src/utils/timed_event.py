from __future__ import annotations

from datetime import datetime, timedelta
from typing import Protocol


class TimedEvent(Protocol):
    start_time_utc: datetime
    duration: timedelta

    @property
    def end_time_utc(self) -> datetime:
        return self.start_time_utc + self.duration

    def intersects_with(self, other: TimedEvent) -> bool:
        return other.start_time_utc < self.end_time_utc and self.start_time_utc < other.end_time_utc
