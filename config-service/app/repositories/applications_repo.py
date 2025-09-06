from __future__ import annotations

"""Raw SQL repository for `applications` table."""

from typing import Optional

from app.db.pool import DBPool


class ApplicationsRepo:
    """Encapsulates CRUD operations for applications."""

    def __init__(self, db: DBPool):
        """Store the connection pool wrapper for later queries."""
        self.db = db

    def create(self, id: str, name: str, comments: Optional[str]) -> dict:
        """Insert a new application and return the persisted row."""
        with self.db.cursor() as (conn, cur):
            cur.execute(
                "INSERT INTO applications (id, name, comments) VALUES (%s, %s, %s) RETURNING id, name, comments",
                (id, name, comments),
            )
            row = cur.fetchone()
            conn.commit()
            return dict(row)

    def update(self, id: str, name: Optional[str], comments: Optional[str]) -> Optional[dict]:
        """Patch fields on an application and return the updated row if found."""
        sets = []
        vals = []
        if name is not None:
            sets.append("name = %s")
            vals.append(name)
        if comments is not None:
            sets.append("comments = %s")
            vals.append(comments)
        if not sets:
            return self.get(id)
        vals.append(id)
        sql = f"UPDATE applications SET {', '.join(sets)} WHERE id = %s RETURNING id, name, comments"
        with self.db.cursor() as (conn, cur):
            cur.execute(sql, vals)
            row = cur.fetchone()
            conn.commit()
            return dict(row) if row else None

    def get(self, id: str) -> Optional[dict]:
        """Return an application by id, or `None` if missing."""
        with self.db.cursor() as (conn, cur):
            cur.execute("SELECT id, name, comments FROM applications WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def list(self) -> list[dict]:
        """List applications ordered by name."""
        with self.db.cursor() as (conn, cur):
            cur.execute("SELECT id, name, comments FROM applications ORDER BY name")
            return [dict(r) for r in cur.fetchall()]

    def get_configuration_ids(self, app_id: str) -> list[str]:
        """List configuration ids for a given application id ordered by name."""
        with self.db.cursor() as (conn, cur):
            cur.execute("SELECT id FROM configurations WHERE application_id = %s ORDER BY name", (app_id,))
            return [r["id"] for r in cur.fetchall()]
