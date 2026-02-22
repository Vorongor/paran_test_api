import pytest

from httpx import AsyncClient, ASGITransport

from pdf_service.pdf_main import app
from pdf_service.security.utils import get_current_user


@pytest.mark.asyncio
async def test_pdf_generation_and_sqs(monkeypatch):
    test_token = "head.payload.signature"
    fake_user = {"email": "test@example.com", "name": "Ivan"}
    app.dependency_overrides[get_current_user] = lambda: fake_user

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        user_data = {
            "id": 1,
            "name": "Ivan",
            "surname": "Tester",
            "email": "test@example.com",
            "date_of_birth": "1995-01-01",
        }
        headers = {"Authorization": f"Bearer {test_token}"}
        response = await ac.post("/pdf/generate", headers=headers, json=user_data)

        assert response.status_code == 200

        response = await ac.post(
            "/pdf/generate-in-storage", headers=headers, json=user_data
        )

        assert response.status_code == 202
