"""
Time utilities.
"""
from datetime import datetime, timezone
from typing import Optional


def utcnow() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Format datetime to ISO string."""
    if dt is None:
        return None
    return dt.isoformat()
