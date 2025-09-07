from __future__ import annotations

import pytest

import httpx

from app.main import app


@pytest.mark.asyncio
async def test_openapi():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/openapi.json")
        assert r.status_code == 200
