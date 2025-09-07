from __future__ import annotations

"""Raw SQL repository for `configurations` table."""

from typing import Optional

from app.db.pool import DBPool
from psycopg2.extras import Json


class ConfigurationsRepo:
    """Encapsulates CRUD operations for configurations."""

    def __init__(self, db: DBPool):
        """Store the connection pool wrapper for later queries."""
        self.db = db

    def create(self, id: str, application_id: str, name: str, comments: Optional[str], config: dict) -> dict:
        """Insert a new configuration row and return it."""
        with self.db.cursor() as (conn, cur):
            cur.execute(
                """
                INSERT INTO configurations (id, application_id, name, comments, config)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, application_id, name, comments, config
                """,
                (id, application_id, name, comments, Json(config)),
            )
            row = cur.fetchone()
            conn.commit()
            return dict(row)

    def update(self, id: str, name: Optional[str], comments: Optional[str], config: Optional[dict]) -> Optional[dict]:
        """Patch fields on a configuration and return the updated row if found."""
        sets = []
        vals = []
        if name is not None:
            sets.append("name = %s")
            vals.append(name)
        if comments is not None:
            sets.append("comments = %s")
            vals.append(comments)
        if config is not None:
            sets.append("config = %s")
            vals.append(Json(config))
        if not sets:
            return self.get(id)
        vals.append(id)
        sql = f"UPDATE configurations SET {', '.join(sets)} WHERE id = %s RETURNING id, application_id, name, comments, config"
        with self.db.cursor() as (conn, cur):
            cur.execute(sql, vals)
            row = cur.fetchone()
            conn.commit()
            return dict(row) if row else None

    def get(self, id: str) -> Optional[dict]:
        """Return a configuration by id, or `None` if missing."""
        with self.db.cursor() as (conn, cur):
            cur.execute(
                "SELECT id, application_id, name, comments, config FROM configurations WHERE id = %s",
                (id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None
