from __future__ import annotations

import httpx

from app.main import app


def test_openapi():
    transport = httpx.ASGITransport(app=app)
    client = httpx.Client(transport=transport, base_url="http://test")
    r = client.get("/openapi.json")
    assert r.status_code == 200
