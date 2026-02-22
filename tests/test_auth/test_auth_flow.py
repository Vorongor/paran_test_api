import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from auth_service.main import app
from auth_service.database.engine import engine
from auth_service.database.base import Base


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.mark.asyncio
async def test_full_auth_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        user_data = {
            "name": "Ivan",
            "surname": "Tester",
            "email": "test@example.com",
            "date_of_birth": "1995-01-01",
            "password": "StrongPassword123!",
        }
        reg_res = await ac.post("/api/v1/users", json=user_data)
        assert reg_res.status_code == 201

        login_res = await ac.post(
            "/api/v1/sessions",
            json={"email": "test@example.com", "password": "StrongPassword123!"},
        )
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        assert token is not None
