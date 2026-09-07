import pytest

def test_csv_report_export(client):
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/api/v1/reports/export/csv", headers=headers)
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]
    assert "Ticket Number,Title,Priority" in resp.text
