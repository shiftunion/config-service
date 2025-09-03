from __future__ import annotations

from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from typing import AsyncIterator

from app.core.config import Settings, get_settings
from app.db.pool import DBPool


executor = ThreadPoolExecutor(max_workers=8)
_pool: DBPool | None = None


def get_pool(settings: Settings | None = None) -> DBPool:
    global _pool
    if _pool is None:
        s = settings or get_settings()
        _pool = DBPool.from_settings(s)
    return _pool


@asynccontextmanager
async def with_pool() -> AsyncIterator[DBPool]:
    yield get_pool()
