from httpx import AsyncClient
import pytest

@pytest.mark.asyncio
async def test_ping(test_client: AsyncClient):
    response = await test_client.get("/health")
    assert response.status_code == 204
    