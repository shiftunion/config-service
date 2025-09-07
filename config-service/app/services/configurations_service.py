from __future__ import annotations

"""Business logic for configuration resources.

Validates and translates low-level database errors into HTTP-friendly
responses and returns typed response models.
"""

from fastapi import HTTPException, status
from psycopg2 import errorcodes

from app.db.pool import DBPool
from app.models.types import ConfigurationCreate, ConfigurationOut, ConfigurationUpdate
from app.repositories.configurations_repo import ConfigurationsRepo


class ConfigurationsService:
    """Service orchestrating CRUD for configurations."""

    def __init__(self, db: DBPool):
        """Initialize with a connection pool-backed repository."""
        self.repo = ConfigurationsRepo(db)

    def create(self, data: ConfigurationCreate) -> ConfigurationOut:
        """Create a configuration; 409 on name conflict, 400 on bad app id."""
        try:
            row = self.repo.create(str(data.id), str(data.application_id), data.name, data.comments, data.config)
        except Exception as e:
            code = getattr(e, "pgcode", None)
            if code == errorcodes.UNIQUE_VIOLATION:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Configuration name must be unique per application")
            if code == errorcodes.FOREIGN_KEY_VIOLATION:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="application_id does not exist")
            raise
        return ConfigurationOut(**row)

    def update(self, id: str, data: ConfigurationUpdate) -> ConfigurationOut:
        """Update a configuration; 404 if missing; 409 on name conflict."""
        try:
            row = self.repo.update(id, data.name, data.comments, data.config)
        except Exception as e:
            code = getattr(e, "pgcode", None)
            if code == errorcodes.UNIQUE_VIOLATION:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Configuration name must be unique per application")
            raise
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuration not found")
        return ConfigurationOut(**row)

    def get(self, id: str) -> ConfigurationOut:
        """Fetch a configuration by id or raise 404."""
        row = self.repo.get(id)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuration not found")
        return ConfigurationOut(**row)
