from __future__ import annotations

from typing import Optional

from app.db.pool import DBPool


class ApplicationsRepo:
    def __init__(self, db: DBPool):
        self.db = db

    def create(self, id: str, name: str, comments: Optional[str]) -> dict:
        with self.db.cursor() as (conn, cur):
            cur.execute(
                "INSERT INTO applications (id, name, comments) VALUES (%s, %s, %s) RETURNING id, name, comments",
                (id, name, comments),
            )
            row = cur.fetchone()
            conn.commit()
            return dict(row)

    def update(self, id: str, name: Optional[str], comments: Optional[str]) -> Optional[dict]:
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
        with self.db.cursor() as (conn, cur):
            cur.execute("SELECT id, name, comments FROM applications WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def list(self) -> list[dict]:
        with self.db.cursor() as (conn, cur):
            cur.execute("SELECT id, name, comments FROM applications ORDER BY name")
            return [dict(r) for r in cur.fetchall()]

    def get_configuration_ids(self, app_id: str) -> list[str]:
        with self.db.cursor() as (conn, cur):
            cur.execute("SELECT id FROM configurations WHERE application_id = %s ORDER BY name", (app_id,))
            return [r["id"] for r in cur.fetchall()]
