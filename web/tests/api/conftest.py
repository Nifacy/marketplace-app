import pytest_asyncio
from fastapi.testclient import TestClient

from app import app


@pytest_asyncio.fixture
async def test_client():
    async with app.lifespan(app.app):
        yield TestClient(app.app)
