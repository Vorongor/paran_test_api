import pytest
from httpx import AsyncClient, ASGITransport

from src.config import get_settings
from src.database import Base
from src.database.engine import engine
from src.main import app


settings = get_settings()


@pytest.mark.asyncio
async def test_register_and_login_flow():
    """
    Test flow for registering and login then retrieve new user
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        user_data = {
            "name": "Ivan",
            "surname": "Tester",
            "email": "test_user_unique@example.com",
            "date_of_birth": "1995-01-01",
            "password": "strongPassword!123"
        }

        response = await ac.post("/api/v1/register", json=user_data)
        assert response.status_code in [200, 201]

        login_data = {
            "email": "test_user_unique@example.com",
            "password": "strongPassword!123"
        }
        login_response = await ac.post("/api/v1/login", json=login_data)

        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

        token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        profile_response = await ac.get("/api/v1/profile", headers=headers)

        assert profile_response.status_code == 200
        assert profile_response.headers["content-type"] == "application/pdf"