from __future__ import annotations

"""Minimal SQL migrations runner for PostgreSQL.

Supports three commands:
- `status`: list known migration files and which are applied
- `up`: apply all pending `.sql` files in lexical order
- `verify`: detect checksum drift for already-applied files
"""

import argparse
import hashlib
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor


MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def env(key: str, default: str | None = None) -> str:
    """Read an env var or exit if missing and no default is provided."""
    val = os.getenv(key, default)
    if val is None:
        raise SystemExit(f"Missing required env var: {key}")
    return val


def db_conn_str() -> str:
    """Build a psycopg2 DSN using env vars with sensible defaults.

    Defaults mirror local dev/docker-compose values so tests can run
    without exporting env variables explicitly.
    """
    host = env("DB_HOST", "localhost")
    port = env("DB_PORT", "5432")
    db = env("DB_NAME", "configsvc-alpha")
    user = env("DB_USER", "postgres")
    pwd = env("DB_PASSWORD", "postgres")
    return f"host={host} port={port} dbname={db} user={user} password={pwd}"


def ensure_bootstrap(conn) -> None:
    """Create the `migrations` bookkeeping table if it does not exist."""
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS migrations (
              id SERIAL PRIMARY KEY,
              filename TEXT NOT NULL UNIQUE,
              checksum TEXT NOT NULL,
              applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
    conn.commit()


def file_checksum(path: Path) -> str:
    """Return SHA-256 checksum for a migration file."""
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()


@dataclass
class Migration:
    filename: str
    checksum: str
    applied: bool


def get_status(conn) -> list[Migration]:
    """Return migration rows combining on-disk files with applied records."""
    ensure_bootstrap(conn)
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT filename, checksum FROM migrations ORDER BY filename")
        applied = {row["filename"]: row["checksum"] for row in cur.fetchall()}

    migrations = []
    for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        cs = file_checksum(path)
        mig = Migration(filename=path.name, checksum=cs, applied=path.name in applied)
        migrations.append(mig)
    return migrations


def apply_up(conn) -> None:
    """Apply all pending migration files in lexical order as a series of txns."""
    ensure_bootstrap(conn)
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT filename, checksum FROM migrations")
        applied = {row["filename"]: row["checksum"] for row in cur.fetchall()}

    for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        cs = file_checksum(path)
        if path.name in applied:
            # Skip already applied
            continue
        sql = path.read_text()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                cur.execute(
                    "INSERT INTO migrations (filename, checksum) VALUES (%s, %s)",
                    (path.name, cs),
                )


def verify(conn) -> list[tuple[str, str, str]]:
    """Return list of (filename, expected_checksum, actual_checksum) if drift detected."""
    ensure_bootstrap(conn)
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT filename, checksum FROM migrations")
        applied = {row["filename"]: row["checksum"] for row in cur.fetchall()}

    drifts: list[tuple[str, str, str]] = []
    for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        if path.name in applied:
            actual = file_checksum(path)
            expected = applied[path.name]
            if actual != expected:
                drifts.append((path.name, expected, actual))
    return drifts


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint; parse args and run the requested command."""
    parser = argparse.ArgumentParser(description="Migrations runner")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("up")
    sub.add_parser("verify")
    args = parser.parse_args(argv)

    conn = psycopg2.connect(db_conn_str())
    try:
        if args.cmd == "status":
            rows = get_status(conn)
            for r in rows:
                status = "APPLIED" if r.applied else "PENDING"
                print(f"{status}\t{r.filename}\t{r.checksum}")
            return 0
        elif args.cmd == "up":
            apply_up(conn)
            print("Migrations applied (if any pending).")
            return 0
        elif args.cmd == "verify":
            drift = verify(conn)
            if drift:
                print("Checksum drift detected:")
                for fn, exp, act in drift:
                    print(f"- {fn}: expected {exp}, actual {act}")
                return 2
            print("No checksum drift.")
            return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
