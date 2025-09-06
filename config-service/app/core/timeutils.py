from __future__ import annotations

"""Time utilities used across the service."""

from datetime import timezone, datetime


def utcnow() -> datetime:
    """Return a timezone-aware UTC `datetime` for consistent timestamps."""
    return datetime.now(timezone.utc)
