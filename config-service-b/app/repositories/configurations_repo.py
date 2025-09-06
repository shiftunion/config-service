"""
Configurations repository.
"""
import json
from typing import List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from app.db import pool
from app.db.sql import (
    CONFIGURATIONS_EXISTS,
    CONFIGURATIONS_INSERT,
    CONFIGURATIONS_SELECT,
    CONFIGURATIONS_SELECT_BY_APP,
    CONFIGURATIONS_SELECT_BY_APP_AND_NAME,
    CONFIGURATIONS_SELECT_BY_ID,
    CONFIGURATIONS_UPDATE,
)
from app.models.types import Configuration, ConfigurationCreate


class ConfigurationsRepository:
    """Repository for configurations data access."""

    @staticmethod
    async def get_all() -> List[Configuration]:
        """Get all configurations."""
        async with pool.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(CONFIGURATIONS_SELECT)
                rows = cursor.fetchall()

        return [Configuration(**row) for row in rows]

    @staticmethod
    async def get_by_id(configuration_id: str) -> Optional[Configuration]:
        """Get configuration by ID."""
        async with pool.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(CONFIGURATIONS_SELECT_BY_ID, (configuration_id,))
                row = cursor.fetchone()

        return Configuration(**row) if row else None

    @staticmethod
    async def get_by_app_and_name(application_id: str, name: str) -> Optional[Configuration]:
        """Get configuration by application ID and name."""
        async with pool.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(CONFIGURATIONS_SELECT_BY_APP_AND_NAME, (application_id, name))
                row = cursor.fetchone()

        return Configuration(**row) if row else None

    @staticmethod
    async def get_by_application(application_id: str) -> List[Configuration]:
        """Get all configurations for application."""
        async with pool.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(CONFIGURATIONS_SELECT_BY_APP, (application_id,))
                rows = cursor.fetchall()

        return [Configuration(**row) for row in rows]

    @staticmethod
    async def create(configuration: ConfigurationCreate, configuration_id: str) -> Configuration:
        """Create new configuration."""
        async with pool.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    CONFIGURATIONS_INSERT,
                    (
                        configuration_id,
                        str(configuration.application_id),
                        configuration.name,
                        configuration.comments,
                        json.dumps(configuration.config)
                    )
                )
                conn.commit()

                # Return created configuration
                cursor.execute(CONFIGURATIONS_SELECT_BY_ID, (configuration_id,))
                row = cursor.fetchone()

        # Convert JSONB string back to dict
        if row and 'config' in row:
            row['config'] = json.loads(row['config'])

        return Configuration(**row) if row else None

    @staticmethod
    async def update(configuration_id: str, configuration: ConfigurationCreate) -> Optional[Configuration]:
        """Update configuration."""
        async with pool.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    CONFIGURATIONS_UPDATE,
                    (
                        configuration.name,
                        configuration.comments,
                        json.dumps(configuration.config),
                        configuration_id
                    )
                )
                conn.commit()

                if cursor.rowcount == 0:
                    return None

                # Return updated configuration
                cursor.execute(CONFIGURATIONS_SELECT_BY_ID, (configuration_id,))
                row = cursor.fetchone()

        # Convert JSONB string back to dict
        if row and 'config' in row:
            row['config'] = json.loads(row['config'])

        return Configuration(**row) if row else None

    @staticmethod
    async def delete(configuration_id: str) -> bool:
        """Delete configuration."""
        async with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(CONFIGURATIONS_EXISTS, (configuration_id,))
                exists = cursor.fetchone() is not None

                if not exists:
                    return False

                cursor.execute("DELETE FROM configurations WHERE id = %s", (configuration_id,))
                conn.commit()

        return cursor.rowcount > 0

    @staticmethod
    async def exists(configuration_id: str) -> bool:
        """Check if configuration exists."""
        async with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(CONFIGURATIONS_EXISTS, (configuration_id,))
                return cursor.fetchone() is not None

    @staticmethod
    async def exists_by_app_and_name(application_id: str, name: str) -> bool:
        """Check if configuration exists by application and name."""
        async with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM configurations WHERE application_id = %s AND name = %s",
                    (application_id, name)
                )
                return cursor.fetchone() is not None
