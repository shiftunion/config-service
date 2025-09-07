from __future__ import annotations

import re
import psycopg2  # type: ignore
"""Test configuration & shared fixtures.

This file centralizes reusable pytest fixtures for the test suite. Key goals:

1. Ensure the service package (``app``) is importable when tests are invoked
     from the project root or the ``config-service`` directory.
2. Apply database migrations once per test session so individual tests focus
     on data logic, not schema setup.
3. Provide a clean database state for each test via table truncation.
4. Offer common helpers (e.g., a compiled ULID regex) to avoid duplication.

Design choices:
- We modify ``sys.path`` instead of installing the package because the project
    uses a simple layout without an editable install step.
- Truncation (rather than transaction rollbacks) is used for simplicity. For a
    larger suite or performance-sensitive CI, a session-level transaction + savepoint
    strategy could be substituted.
- Fixtures are intentionally *lightweight* and avoid hidden magic—each test
    can still explicitly arrange data using repositories or services.
"""

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
    """Apply (or verify) all migrations once for the session.

    Idempotent: if migrations already applied, re-running causes no changes.
    This keeps each test focused on data behavior rather than schema setup.
    """
    conn = psycopg2.connect(migrations.db_conn_str())
    try:
        migrations.apply_up(conn)
    finally:
        conn.close()


@pytest.fixture(autouse=True)
def _clean_db():
    """Truncate mutable tables before each test for isolation.

    Simplicity over speed: TRUNCATE is acceptable for the current scale.
    If performance becomes an issue, switch to a transaction + rollback strategy.
    """
    pool = get_pool()
    with pool.cursor() as (conn, cur):
        cur.execute("TRUNCATE configurations CASCADE;")
        cur.execute("TRUNCATE applications CASCADE;")
        conn.commit()
    yield


@pytest.fixture
def ulid_regex():
    """Compiled regex for validating canonical 26-char Crockford Base32 ULIDs."""
    return re.compile(r"^[0-9A-HJKMNP-TV-Z]{26}$")
