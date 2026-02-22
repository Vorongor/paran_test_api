import pytest
import httpx
import time

AUTH_URL = "http://auth_api:8000/api/v1"
PDF_URL = "http://pdf_service:8001/api/v1"


@pytest.fixture(scope="module")
def client():
    return httpx.Client(timeout=10.0)


def test_full_user_lifecycle(client):
    user_data = {
        "name": "E2E",
        "surname": "Tester",
        "email": f"e2e_{time.time()}@example.com",
        "date_of_birth": "1990-01-01",
        "password": "Password123!",
    }
    reg_res = client.post(f"{AUTH_URL}/users", json=user_data)
    assert reg_res.status_code == 201

    login_res = client.post(
        f"{AUTH_URL}/sessions",
        json={"email": user_data["email"], "password": user_data["password"]},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    pdf_res = client.get(f"{AUTH_URL}/me/profile", headers=headers)
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"

    s3_res = client.get(f"{AUTH_URL}/me/profile-in-storage", headers=headers)
    assert s3_res.status_code == 202

    logout_res = client.post(f"{AUTH_URL}/logout", headers=headers)
    assert logout_res.status_code in [200, 204]

    client.post(f"{AUTH_URL}/logout", headers=headers)

    retry_pdf = client.get(f"{AUTH_URL}/me/profile", headers=headers)
    assert retry_pdf.status_code == 401
