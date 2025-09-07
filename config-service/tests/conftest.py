from __future__ import annotations

import re
import psycopg2  # type: ignore
import pytest

import sys
from pathlib import Path

# Ensure project root (where 'app' package lives) is on sys.path when tests are run
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.api.deps import get_pool  # noqa: E402
from app.core import config as config_mod  # noqa: E402

import migrations


@pytest.fixture(scope="session", autouse=True)
def _apply_migrations():
    """Ensure database schema is up before any tests run."""
    conn = psycopg2.connect(migrations.db_conn_str())
    try:
        migrations.apply_up(conn)
    finally:
        conn.close()


@pytest.fixture(autouse=True)
def _clean_db():
    """Truncate data tables for isolation between tests."""
    pool = get_pool()
    with pool.cursor() as (conn, cur):
        cur.execute("TRUNCATE configurations CASCADE;")
        cur.execute("TRUNCATE applications CASCADE;")
        conn.commit()
    yield


@pytest.fixture
def ulid_regex():
    # Crockford base32 (no I,L,O,U) 26 chars
    return re.compile(r"^[0-9A-HJKMNP-TV-Z]{26}$")
