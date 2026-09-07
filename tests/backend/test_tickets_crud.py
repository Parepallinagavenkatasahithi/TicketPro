import pytest

def test_create_and_get_ticket(client):
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "employee.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create ticket
    create_resp = client.post("/api/v1/tickets", json={
        "title": "VPN connection drops on Linux",
        "description": "Connecting via OpenVPN causes packet loss every 10 minutes",
        "category_id": 1,
        "priority": "HIGH"
    }, headers=headers)
    assert create_resp.status_code == 201
    ticket_data = create_resp.json()
    assert "ticket_number" in ticket_data
    ticket_id = ticket_data["id"]

    # Get ticket detail
    get_resp = client.get(f"/api/v1/tickets/{ticket_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "VPN connection drops on Linux"
