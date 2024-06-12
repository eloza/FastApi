import pytest
from httpx import AsyncClient
from uuid import UUID, uuid4
from fastapi import FastAPI
from main import app

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
    # based on the initial db size
    assert len(response.json()) == 2 

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

# Testing User Deletion
@pytest.mark.asyncio
async def test_delete_user(client, setup_user):
    # Assuming setup_user adds a user and returns the ID
    user_id = setup_user()
    response = await client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200

    response = await client.get("/api/v1/users")
    assert user_id not in [user['id'] for user in response.json()]
