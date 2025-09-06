"""
Applications repository.
"""
import json
from typing import List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from app.db import pool
from app.db.sql import (
    APPLICATIONS_EXISTS,
    APPLICATIONS_INSERT,
    APPLICATIONS_SELECT,
    APPLICATIONS_SELECT_BY_ID,
    APPLICATIONS_SELECT_BY_NAME,
    APPLICATIONS_UPDATE,
    APPLICATIONS_WITH_CONFIG_COUNT,
    APPLICATIONS_WITH_CONFIG_COUNT_BY_ID,
)
from app.models.types import Application, ApplicationCreate


class ApplicationsRepository:
    """Repository for applications data access."""

    @staticmethod
    async def get_all() -> List[Application]:
        """Get all applications."""
        async with pool.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(APPLICATIONS_SELECT)
                rows = cursor.fetchall()

        return [Application(**row) for row in rows]

    @staticmethod
    async def get_by_id(application_id: str) -> Optional[Application]:
        """Get application by ID."""
        async with pool.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(APPLICATIONS_SELECT_BY_ID, (application_id,))
                row = cursor.fetchone()

        return Application(**row) if row else None

    @staticmethod
    async def get_by_name(name: str) -> Optional[Application]:
        """Get application by name."""
        async with pool.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(APPLICATIONS_SELECT_BY_NAME, (name,))
                row = cursor.fetchone()

        return Application(**row) if row else None

    @staticmethod
    async def create(application: ApplicationCreate, application_id: str) -> Application:
        """Create new application."""
        async with pool.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    APPLICATIONS_INSERT,
                    (application_id, application.name, application.comments)
                )
                conn.commit()

                # Return created application
                cursor.execute(APPLICATIONS_SELECT_BY_ID, (application_id,))
                row = cursor.fetchone()

        return Application(**row)

    @staticmethod
    async def update(application_id: str, application: ApplicationCreate) -> Optional[Application]:
        """Update application."""
        async with pool.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    APPLICATIONS_UPDATE,
                    (application.name, application.comments, application_id)
                )
                conn.commit()

                if cursor.rowcount == 0:
                    return None

                # Return updated application
                cursor.execute(APPLICATIONS_SELECT_BY_ID, (application_id,))
                row = cursor.fetchone()

        return Application(**row) if row else None

    @staticmethod
    async def delete(application_id: str) -> bool:
        """Delete application."""
        async with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(APPLICATIONS_EXISTS, (application_id,))
                exists = cursor.fetchone() is not None

                if not exists:
                    return False

                cursor.execute("DELETE FROM applications WHERE id = %s", (application_id,))
                conn.commit()

        return cursor.rowcount > 0

    @staticmethod
    async def exists(application_id: str) -> bool:
        """Check if application exists."""
        async with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(APPLICATIONS_EXISTS, (application_id,))
                return cursor.fetchone() is not None

    @staticmethod
    async def get_configuration_ids(application_id: str) -> List[str]:
        """Get configuration IDs for application."""
        async with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM configurations WHERE application_id = %s",
                    (application_id,)
                )
                rows = cursor.fetchall()

        return [row[0] for row in rows]
