import pytest
from httpx import AsyncClient
from uuid import UUID, uuid4
from fastapi import FastAPI
from main import app  # Adjust the import according to your project structure

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Testing root endpoint
@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}

# Testing User Listing
@pytest.mark.asyncio
async def test_fetch_users(client):
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    assert len(response.json()) == 2  # based on the initial db size

# Testing User Registration
@pytest.mark.asyncio
async def test_register_user(client):
    new_user = {
        "id": str(uuid4()),
        "first_name": "Riff",
        "last_name": "Raff",
        "gender": "male",
        "roles": ["admin"]
    }
    response = await client.post("/api/v1/users", json=new_user)
    assert response.status_code == 200
    assert UUID(response.json()["id"]) == UUID(new_user["id"])
