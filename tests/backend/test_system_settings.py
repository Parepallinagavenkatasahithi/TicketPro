import pytest

def test_system_settings_get(client):
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/api/v1/system/settings", headers=headers)
    assert resp.status_code == 200
