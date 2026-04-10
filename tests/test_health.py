from unittest.mock import AsyncMock, patch

from httpx import AsyncClient


async def test_health_all_connected(client: AsyncClient):
    """Qdrant, LiteLLM 모두 연결되면 status=ok."""
    with (
        patch("app.api.health.VectorProvider.check_connection", new_callable=AsyncMock, return_value=True),
        patch("app.api.health.LLMProvider.check_connection", new_callable=AsyncMock, return_value=True),
    ):
        resp = await client.get("/health")

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["qdrant"] == "connected"
    assert data["litellm"] == "connected"


async def test_health_qdrant_down(client: AsyncClient):
    """Qdrant 다운 시 status=degraded."""
    with (
        patch("app.api.health.VectorProvider.check_connection", new_callable=AsyncMock, return_value=False),
        patch("app.api.health.LLMProvider.check_connection", new_callable=AsyncMock, return_value=True),
    ):
        resp = await client.get("/health")

    assert resp.status_code == 503
    data = resp.json()
    assert data["status"] == "degraded"
    assert data["qdrant"] == "disconnected"


async def test_health_litellm_down(client: AsyncClient):
    """LiteLLM 다운 시 status=degraded."""
    with (
        patch("app.api.health.VectorProvider.check_connection", new_callable=AsyncMock, return_value=True),
        patch("app.api.health.LLMProvider.check_connection", new_callable=AsyncMock, return_value=False),
    ):
        resp = await client.get("/health")

    assert resp.status_code == 503
    data = resp.json()
    assert data["status"] == "degraded"
    assert data["litellm"] == "disconnected"
