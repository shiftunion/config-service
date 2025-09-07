from __future__ import annotations

from fastapi.testclient import TestClient
from pydantic_extra_types.ulid import ULID

from app.main import app

client = TestClient(app)


def test_create_application_and_get(ulid_regex):
    r = client.post("/api/v1/applications", json={"id": str(ULID()), "name": "api-app", "comments": "c"})
    assert r.status_code == 201
    data = r.json()
    assert data["id"]
    rid = data["id"]
    g = client.get(f"/api/v1/applications/{rid}")
    assert g.status_code == 200
    assert g.json()["configuration_ids"] == []


def test_duplicate_application_name():
    nm = "dup-api"
    client.post("/api/v1/applications", json={"id": str(ULID()), "name": nm, "comments": None})
    r = client.post("/api/v1/applications", json={"id": str(ULID()), "name": nm, "comments": None})
    assert r.status_code == 409


def test_get_missing_application():
    r = client.get(f"/api/v1/applications/{ULID()}")
    assert r.status_code == 404


def test_configuration_fk_and_success():
    app_resp = client.post("/api/v1/applications", json={"id": str(ULID()), "name": "cfg-app", "comments": None})
    app_id = app_resp.json()["id"]
    bad = client.post(
        "/api/v1/configurations",
        json={"id": str(ULID()), "application_id": str(ULID()), "name": "bad", "comments": None, "config": {"x": 1}},
    )
    assert bad.status_code in (400, 404, 422)
    good = client.post(
        "/api/v1/configurations",
        json={"id": str(ULID()), "application_id": app_id, "name": "good", "comments": "c", "config": {"x": True}},
    )
    assert good.status_code == 201
    conf_id = good.json()["id"]
    got = client.get(f"/api/v1/configurations/{conf_id}")
    assert got.status_code == 200
    assert got.json()["config"]["x"] is True
