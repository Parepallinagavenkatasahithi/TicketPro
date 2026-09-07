import pytest

def test_assign_ticket(client):
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Create ticket
    t_resp = client.post("/api/v1/tickets", json={
        "title": "Hardware laptop screen flicker",
        "description": "Screen flickers on cold boot",
        "category_id": 1,
        "priority": "MEDIUM"
    }, headers=admin_headers)
    ticket_id = t_resp.json()["id"]

    # Assign ticket to agent
    assign_resp = client.put(f"/api/v1/tickets/{ticket_id}/assign", json={
        "agent_id": 2,
        "reason": "Reassigning to tier 1 specialist"
    }, headers=admin_headers)
    assert assign_resp.status_code == 200
    assert assign_resp.json()["assigned_agent_id"] == 2
