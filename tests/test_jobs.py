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


async def test_list_jobs(client: AsyncClient):
    await client.post(
        "/api/v1/jobs",
        json={"site_address": "1 List Test Rd", "description": "List test job"},
    )
    response = await client.get("/api/v1/jobs")
    assert response.status_code == 200
    data = response.json()
    assert any(job["site_address"] == "1 List Test Rd" for job in data)


async def test_get_job_by_id(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/jobs",
        json={"site_address": "2 Get Test Ave", "description": "Get test job"},
    )
    job_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job_id
    assert data["site_address"] == "2 Get Test Ave"


async def test_get_job_not_found(client: AsyncClient):
    response = await client.get("/api/v1/jobs/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"
