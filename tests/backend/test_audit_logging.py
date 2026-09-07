import pytest

def test_audit_logs_query(client):
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/api/v1/audit", headers=headers)
    assert resp.status_code == 200
    logs = resp.json()
    assert len(logs) >= 1
