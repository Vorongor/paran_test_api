import pytest
import respx
from httpx import AsyncClient, ASGITransport, Response

from src.config import get_settings
from src.database import Base
from src.database.engine import engine
from src.main import app

settings = get_settings()


@pytest.mark.asyncio
@respx.mock
async def test_register_and_login_flow():
    """
    Test flow for registering and login then retrieve new user
    """
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    pdf_route = respx.post("http://pdf_service:8001/generate").mock(
        return_value=Response(
            200,
            content=b"fake_pdf_content",
            headers={"Content-Type": "application/pdf"}
        )
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        user_data = {
            "name": "Ivan",
            "surname": "Tester",
            "email": "test_user_unique@example.com",
            "date_of_birth": "1995-01-01",
            "password": "strongPassword!123",
        }
        response = await ac.post("/api/v1/users", json=user_data)
        assert response.status_code == 201

        login_data = {
            "email": "test_user_unique@example.com",
            "password": "strongPassword!123",
        }
        login_response = await ac.post("/api/v1/sessions", json=login_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        profile_response = await ac.get("/api/v1/me/profile", headers=headers)

        assert profile_response.status_code == 200
        assert profile_response.headers["content-type"] == "application/pdf"
        assert profile_response.content == b"fake_pdf_content"

        assert pdf_route.called