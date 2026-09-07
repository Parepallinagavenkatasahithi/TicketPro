import pytest

def test_dashboard_analytics_endpoints(client):
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    dash_resp = client.get("/api/v1/analytics/dashboard", headers=headers)
    assert dash_resp.status_code == 200
    data = dash_resp.json()
    assert "total_tickets" in data
    assert "sla_compliance_rate" in data

    trends_resp = client.get("/api/v1/analytics/trends", headers=headers)
    assert trends_resp.status_code == 200
    assert len(trends_resp.json()) == 7
