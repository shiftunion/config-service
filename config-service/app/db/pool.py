from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor

from app.core.config import Settings


@dataclass
class DBPool:
    pool: ThreadedConnectionPool

    @classmethod
    def from_settings(cls, settings: Settings) -> "DBPool":
        dsn = (
            f"host={settings.DB_HOST} port={settings.DB_PORT} dbname={settings.DB_NAME} "
            f"user={settings.DB_USER} password={settings.DB_PASSWORD}"
        )
        pool = ThreadedConnectionPool(
            minconn=settings.DB_POOL_MIN,
            maxconn=settings.DB_POOL_MAX,
            dsn=dsn,
        )
        return cls(pool)

    @contextmanager
    def get_conn(self):
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)

    @contextmanager
    def cursor(self):
        with self.get_conn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    yield conn, cur
                except Exception:
                    try:
                        conn.rollback()
                    finally:
                        pass
                    raise
