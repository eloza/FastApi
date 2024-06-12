import pytest
from httpx import AsyncClient
from uuid import UUID
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
