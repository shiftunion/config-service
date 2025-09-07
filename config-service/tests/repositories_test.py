from __future__ import annotations

import psycopg2
import pytest
from psycopg2 import errors

from app.api.deps import get_pool
from app.repositories.applications_repo import ApplicationsRepo
from app.repositories.configurations_repo import ConfigurationsRepo


@pytest.fixture
def repos():
    pool = get_pool()
    return ApplicationsRepo(pool), ConfigurationsRepo(pool)


def test_applications_crud(repos):
    apps_repo, _ = repos
    a = apps_repo.create("A1", "app-one", "c1")
    got = apps_repo.get(a["id"])
    assert got["name"] == "app-one"
    listed = apps_repo.list()
    assert any(r["id"] == a["id"] for r in listed)


def test_application_unique_violation(repos):
    apps_repo, _ = repos
    apps_repo.create("A2", "dup-app", None)
    with pytest.raises(Exception):
        apps_repo.create("A3", "dup-app", None)


def test_configurations_fk_and_unique(repos):
    apps_repo, configs_repo = repos
    apps_repo.create("APPX", "app-x", None)
    c = configs_repo.create("C1", "APPX", "cfg", None, {"k": 1})
    got = configs_repo.get(c["id"])
    assert got["config"]["k"] == 1
    # Unique per app
    with pytest.raises(Exception):
        configs_repo.create("C2", "APPX", "cfg", None, {"k": 2})
    # FK violation (different app id)
    with pytest.raises(Exception):
        configs_repo.create("C3", "NOPE", "other", None, {})
