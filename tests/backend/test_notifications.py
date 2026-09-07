import pytest

def test_notifications_lifecycle(client):
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    notifs_resp = client.get("/api/v1/notifications", headers=headers)
    assert notifs_resp.status_code == 200

    read_all_resp = client.put("/api/v1/notifications/read-all", headers=headers)
    assert read_all_resp.status_code == 200
