#!/usr/bin/env python3
"""
Database migrations CLI tool.
"""
import hashlib
import logging
import sys
from pathlib import Path
from typing import List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

# Add app to path for imports
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def get_connection():
    """Get database connection."""
    settings = get_settings()
    return psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        cursor_factory=RealDictCursor
    )


def create_migrations_table(conn):
    """Create migrations table if it doesn't exist."""
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id SERIAL PRIMARY KEY,
                filename TEXT NOT NULL UNIQUE,
                checksum TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()


def calculate_checksum(content: str) -> str:
    """Calculate SHA256 checksum of migration content."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def get_migration_files() -> List[Path]:
    """Get sorted list of migration files."""
    migrations_dir = Path(__file__).parent / "migrations"
    return sorted(migrations_dir.glob("*.sql"))


def get_applied_migrations(conn) -> dict:
    """Get dict of applied migrations filename -> checksum."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT filename, checksum FROM migrations")
        return {row['filename']: row['checksum'] for row in cursor.fetchall()}


def status():
    """Show migration status."""
    try:
        conn = get_connection()
        create_migrations_table(conn)

        applied = get_applied_migrations(conn)
        files = get_migration_files()

        print("Migration Status:")
        print("=" * 50)

        for file_path in files:
            filename = file_path.name
            with open(file_path) as f:
                content = f.read()
            checksum = calculate_checksum(content)

            if filename in applied:
                status_text = "APPLIED"
                if applied[filename] != checksum:
                    status_text = "CHECKSUM MISMATCH"
                print(f"{filename}: {status_text}")
            else:
                print(f"{filename}: PENDING")

        conn.close()

    except Exception as e:
        logger.error(f"Error checking migration status: {e}")
        sys.exit(1)


def up():
    """Apply pending migrations."""
    try:
        conn = get_connection()
        create_migrations_table(conn)

        applied = get_applied_migrations(conn)
        files = get_migration_files()

        applied_any = False
        for file_path in files:
            filename = file_path.name

            if filename in applied:
                continue

            print(f"Applying migration: {filename}")

            with open(file_path) as f:
                content = f.read()

            checksum = calculate_checksum(content)

            # Execute migration
            with conn.cursor() as cursor:
                cursor.execute(content)

                # Record migration
                cursor.execute(
                    "INSERT INTO migrations (filename, checksum) VALUES (%s, %s)",
                    (filename, checksum)
                )

            conn.commit()
            applied_any = True
            print(f"✓ Applied {filename}")

        if not applied_any:
            print("No pending migrations.")

        conn.close()

    except Exception as e:
        logger.error(f"Error applying migrations: {e}")
        sys.exit(1)


def verify():
    """Verify applied migrations match current checksums."""
    try:
        conn = get_connection()
        create_migrations_table(conn)

        applied = get_applied_migrations(conn)
        files = get_migration_files()

        all_good = True
        for file_path in files:
            filename = file_path.name

            if filename not in applied:
                continue

            with open(file_path) as f:
                content = f.read()

            checksum = calculate_checksum(content)
            stored_checksum = applied[filename]

            if checksum != stored_checksum:
                print(f"❌ Checksum mismatch for {filename}")
                all_good = False
            else:
                print(f"✓ {filename} checksum verified")

        if all_good:
            print("All applied migrations verified successfully.")
        else:
            print("Some migrations have checksum mismatches.")
            sys.exit(1)

        conn.close()

    except Exception as e:
        logger.error(f"Error verifying migrations: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    if len(sys.argv) != 2:
        print("Usage: python migrations.py <command>")
        print("Commands: status, up, verify")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "status":
        status()
    elif command == "up":
        up()
    elif command == "verify":
        verify()
    else:
        print(f"Unknown command: {command}")
        print("Commands: status, up, verify")
        sys.exit(1)


if __name__ == "__main__":
    main()
