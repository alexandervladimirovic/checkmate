from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import Column, DateTime

tz = ZoneInfo("UTC")


def utc_current_time():
    return datetime.now(tz)


class TimeStampMixin:
    created_at = Column(DateTime, default=utc_current_time)
    updated_at = Column(DateTime, default=utc_current_time, onupdate=utc_current_time)

    def update_timestamp(self):
        self.updated_at = datetime.now(tz)
