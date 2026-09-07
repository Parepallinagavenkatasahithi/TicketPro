import pytest
from fastapi.testclient import TestClient

def test_list_and_create_email_templates(client: TestClient, admin_token_headers: dict):
    tmpl_data = {
        "name": "Ticket Resolution Confirmation",
        "event_trigger": "TICKET_RESOLVED",
        "subject_template": "Your Ticket {{ ticket_number }} Has Been Resolved",
        "body_template": "Hello {{ user_name }},\n\nYour ticket {{ ticket_number }} has been marked as resolved by {{ agent_name }}.",
        "description": "Sent automatically when a support ticket status changes to RESOLVED."
    }
    t_res = client.post("/api/v1/email-templates", json=tmpl_data, headers=admin_token_headers)
    assert t_res.status_code == 201
    tmpl = t_res.json()
    assert tmpl["name"] == tmpl_data["name"]

    list_res = client.get("/api/v1/email-templates", headers=admin_token_headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1
