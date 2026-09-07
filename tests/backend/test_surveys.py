import pytest
from fastapi.testclient import TestClient

def test_submit_and_list_surveys(client: TestClient, employee_token_headers: dict, admin_token_headers: dict):
    # 1. Create a ticket first to get a ticket ID
    ticket_payload = {
        "title": "CSAT Test Ticket",
        "description": "Ticket for testing survey submissions",
        "category_id": 1,
        "priority": "MEDIUM"
    }
    t_res = client.post("/api/v1/tickets", json=ticket_payload, headers=employee_token_headers)
    assert t_res.status_code == 201
    ticket_id = t_res.json()["id"]

    # 2. Submit CSAT survey
    survey_payload = {
        "ticket_id": ticket_id,
        "rating": 5,
        "feedback_text": "Excellent support and very quick response time!"
    }
    s_res = client.post("/api/v1/surveys", json=survey_payload, headers=employee_token_headers)
    assert s_res.status_code == 201
    data = s_res.json()
    assert data["rating"] == 5
    assert data["ticket_id"] == ticket_id

    # 3. List surveys as admin
    list_res = client.get("/api/v1/surveys", headers=admin_token_headers)
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) >= 1
    assert any(s["ticket_id"] == ticket_id for s in items)
