from httpx import AsyncClient


async def test_create_job(client: AsyncClient):
    response = await client.post(
        "/api/v1/jobs",
        json={"site_address": "123 Test St", "description": "Test description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["site_address"] == "123 Test St"
    assert data["description"] == "Test description"
    assert data["status"] == "pending"
