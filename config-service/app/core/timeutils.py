from __future__ import annotations

from datetime import timezone, datetime


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
