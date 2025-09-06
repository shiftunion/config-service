from __future__ import annotations

"""Business logic for application resources.

Translates repository/database errors into HTTP exceptions and builds
API-facing response models.
"""

from typing import Optional

from fastapi import HTTPException, status
from psycopg2 import errors

from app.db.pool import DBPool
from app.models.types import ApplicationCreate, ApplicationOut, ApplicationUpdate
from app.repositories.applications_repo import ApplicationsRepo


class ApplicationsService:
    """Service orchestrating CRUD for applications."""

    def __init__(self, db: DBPool):
        """Initialize with a connection pool-backed repository."""
        self.repo = ApplicationsRepo(db)

    def create(self, data: ApplicationCreate) -> ApplicationOut:
        """Create a new application or raise 409 on duplicate name."""
        try:
            row = self.repo.create(str(data.id), data.name, data.comments)
        except Exception as e:  # map unique violation to 409
            if getattr(e, "pgcode", None) == errors.UniqueViolation.sqlstate:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Application name must be unique")
            raise
        conf_ids = self.repo.get_configuration_ids(row["id"])  # empty
        return ApplicationOut(id=row["id"], name=row["name"], comments=row["comments"], configuration_ids=conf_ids)

    def update(self, id: str, data: ApplicationUpdate) -> ApplicationOut:
        """Update an application; raises 404 if not found, 409 on conflict."""
        try:
            row = self.repo.update(id, data.name, data.comments)
        except Exception as e:
            if getattr(e, "pgcode", None) == errors.UniqueViolation.sqlstate:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Application name must be unique")
            raise
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
        conf_ids = self.repo.get_configuration_ids(row["id"])  # could have values
        return ApplicationOut(id=row["id"], name=row["name"], comments=row["comments"], configuration_ids=conf_ids)

    def get(self, id: str) -> ApplicationOut:
        """Fetch an application by id or raise 404."""
        row = self.repo.get(id)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
        conf_ids = self.repo.get_configuration_ids(row["id"])  # could have values
        return ApplicationOut(id=row["id"], name=row["name"], comments=row["comments"], configuration_ids=conf_ids)

    def list(self) -> list[ApplicationOut]:
        """List applications with their related configuration ids."""
        rows = self.repo.list()
        return [ApplicationOut(id=r["id"], name=r["name"], comments=r["comments"], configuration_ids=self.repo.get_configuration_ids(r["id"])) for r in rows]
