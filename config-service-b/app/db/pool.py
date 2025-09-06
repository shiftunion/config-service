"""
Database connection pool.
"""
import contextlib
from concurrent.futures import ThreadPoolExecutor
from typing import Iterator

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

from app.core.config import get_settings

settings = get_settings()

# Global connection pool
_pool: ThreadedConnectionPool = None


def get_pool() -> ThreadedConnectionPool:
    """Get or create connection pool."""
    global _pool
    if _pool is None:
        _pool = ThreadedConnectionPool(
            minconn=settings.db_pool_min_conn,
            maxconn=settings.db_pool_max_conn,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password
        )
    return _pool


def close_pool():
    """Close connection pool."""
    global _pool
    if _pool:
        _pool.closeall()
        _pool = None


@contextlib.asynccontextmanager
async def get_connection():
    """Get database connection from pool (async context manager)."""
    pool = get_pool()
    executor = ThreadPoolExecutor(max_workers=1)

    def _get_conn():
        return pool.getconn()

    def _put_conn(conn):
        pool.putconn(conn)

    try:
        conn = await executor.submit(_get_conn)
        try:
            yield conn
        finally:
            executor.submit(_put_conn, conn)
    finally:
        executor.shutdown(wait=True)


def get_cursor(connection) -> Iterator[RealDictCursor]:
    """Get cursor from connection (context manager)."""
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        yield cursor
