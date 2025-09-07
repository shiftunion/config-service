from __future__ import annotations

import psycopg2

import migrations


def test_status_and_idempotent_up():
    conn = psycopg2.connect(migrations.db_conn_str())
    try:
        before = migrations.get_status(conn)
        migrations.apply_up(conn)
        after = migrations.get_status(conn)
    finally:
        conn.close()
    assert all(m.applied for m in after)
    applied_checksums = {m.filename: m.checksum for m in after}
    conn = psycopg2.connect(migrations.db_conn_str())
    try:
        migrations.apply_up(conn)
        again = migrations.get_status(conn)
    finally:
        conn.close()
    assert {m.filename: m.checksum for m in again} == applied_checksums


def test_checksum_drift_detection():
    conn = psycopg2.connect(migrations.db_conn_str())
    try:
        migrations.apply_up(conn)
    finally:
        conn.close()

    mig_file = next((m for m in migrations.MIGRATIONS_DIR.glob("*.sql")))
    original = mig_file.read_text()
    try:
        mig_file.write_text(original + "-- drift\n")
        conn = psycopg2.connect(migrations.db_conn_str())
        try:
            drift = migrations.verify(conn)
        finally:
            conn.close()
        assert any(d[0] == mig_file.name for d in drift)
    finally:
        mig_file.write_text(original)
