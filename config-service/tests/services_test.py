from __future__ import annotations

import pytest
from pydantic_extra_types.ulid import ULID

from app.api.deps import get_pool
from app.services.applications_service import ApplicationsService
from app.services.configurations_service import ConfigurationsService
from app.models.types import ApplicationCreate, ConfigurationCreate


@pytest.fixture
def services():
    pool = get_pool()
    return ApplicationsService(pool), ConfigurationsService(pool)


def test_application_unique_conflict(services):
    apps_svc, _ = services
    apps_svc.create(ApplicationCreate(id=ULID(), name="svc-app", comments=None))
    with pytest.raises(Exception):
        apps_svc.create(ApplicationCreate(id=ULID(), name="svc-app", comments=None))


def test_configuration_fk_violation(services):
    _, configs_svc = services
    with pytest.raises(Exception):
        configs_svc.create(
            ConfigurationCreate(
                id=ULID(),
                application_id=ULID(),
                name="cfg-x",
                comments=None,
                config={"a": 1},
            )
        )
