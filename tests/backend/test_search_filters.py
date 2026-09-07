import pytest

def test_ticket_search_and_filter(client):
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Search tickets
    resp = client.get("/api/v1/tickets?search=VPN", headers=headers)
    assert resp.status_code == 200
    tickets = resp.json()
    assert isinstance(tickets, list)
