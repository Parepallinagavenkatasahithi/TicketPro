import pytest
from fastapi.testclient import TestClient

def test_log_and_get_time_entries(client: TestClient, admin_token_headers: dict):
    # 1. Create a ticket
    t_res = client.post("/api/v1/tickets", json={
        "title": "Time Tracking Ticket",
        "description": "Log effort hours test",
        "category_id": 1,
        "priority": "HIGH"
    }, headers=admin_token_headers)
    assert t_res.status_code == 201
    ticket_id = t_res.json()["id"]

    # 2. Log time entry
    entry_payload = {
        "ticket_id": ticket_id,
        "hours_spent": 2.5,
        "activity_type": "DEVELOPMENT",
        "description": "Debugging backend database connection pool exhaustion"
    }
    log_res = client.post("/api/v1/time-tracking", json=entry_payload, headers=admin_token_headers)
    assert log_res.status_code == 201
    entry_data = log_res.json()
    assert entry_data["hours_spent"] == 2.5
    assert entry_data["activity_type"] == "DEVELOPMENT"

    # 3. Get time entries for ticket
    get_res = client.get(f"/api/v1/time-tracking/tickets/{ticket_id}", headers=admin_token_headers)
    assert get_res.status_code == 200
    entries = get_res.json()
    assert len(entries) >= 1
    assert entries[0]["hours_spent"] == 2.5
