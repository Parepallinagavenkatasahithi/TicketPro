import pytest

def test_announcements_flow(client):
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = client.post("/api/v1/announcements", json={
        "title": "System Maintenance Notice",
        "content": "Server reboot scheduled at 2 AM",
        "priority": "URGENT",
        "target_audience": "ALL",
        "status": "PUBLISHED"
    }, headers=headers)
    assert create_resp.status_code == 201
    assert create_resp.json()["title"] == "System Maintenance Notice"

    list_resp = client.get("/api/v1/announcements", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1
