from __future__ import annotations

from fastapi import HTTPException, status
from psycopg2 import errors

from app.db.pool import DBPool
from app.models.types import ConfigurationCreate, ConfigurationOut, ConfigurationUpdate
from app.repositories.configurations_repo import ConfigurationsRepo


class ConfigurationsService:
    def __init__(self, db: DBPool):
        self.repo = ConfigurationsRepo(db)

    def create(self, data: ConfigurationCreate) -> ConfigurationOut:
        try:
            row = self.repo.create(str(data.id), str(data.application_id), data.name, data.comments, data.config)
        except Exception as e:
            code = getattr(e, "pgcode", None)
            if code == errors.UniqueViolation.sqlstate:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Configuration name must be unique per application")
            if code == errors.ForeignKeyViolation.sqlstate:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="application_id does not exist")
            raise
        return ConfigurationOut(**row)

    def update(self, id: str, data: ConfigurationUpdate) -> ConfigurationOut:
        try:
            row = self.repo.update(id, data.name, data.comments, data.config)
        except Exception as e:
            code = getattr(e, "pgcode", None)
            if code == errors.UniqueViolation.sqlstate:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Configuration name must be unique per application")
            raise
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuration not found")
        return ConfigurationOut(**row)

    def get(self, id: str) -> ConfigurationOut:
        row = self.repo.get(id)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuration not found")
        return ConfigurationOut(**row)
