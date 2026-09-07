import pytest
import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'backend')))
from app.main import app

import uuid

def test_full_end_to_end_ticket_lifecycle():
    client = TestClient(app)

    unique_email = f"e2e.{uuid.uuid4().hex[:6]}@ticketpro.internal"

    # 1. Register Employee
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": unique_email,
        "password": "Password123!",
        "full_name": "E2E Employee",
        "job_title": "QA Engineer"
    })
    assert reg_resp.status_code == 201
    emp_data = reg_resp.json()

    # 2. Login Employee
    login_resp = client.post("/api/v1/auth/login", json={
        "email": unique_email,
        "password": "Password123!"
    })
    assert login_resp.status_code == 200
    emp_token = login_resp.json()["access_token"]
    emp_headers = {"Authorization": f"Bearer {emp_token}"}

    # 3. Create Ticket
    create_t_resp = client.post("/api/v1/tickets", json={
        "title": "E2E Full Ticket Lifecycle Test",
        "description": "Verifying complete lifecycle from creation to closure",
        "category_id": 1,
        "priority": "HIGH"
    }, headers=emp_headers)
    assert create_t_resp.status_code == 201
    ticket = create_t_resp.json()
    t_id = ticket["id"]
    t_num = ticket["ticket_number"]

    # 4. Login Agent
    agent_login = client.post("/api/v1/auth/login", json={
        "email": "agent.alex@ticketpro.internal",
        "password": "Password123!"
    })
    agent_token = agent_login.json()["access_token"]
    agent_headers = {"Authorization": f"Bearer {agent_token}"}

    # 5. Agent posts response comment
    c_resp = client.post(f"/api/v1/tickets/{t_id}/comments", json={
        "content": "I am working on this ticket right now.",
        "is_internal_note": False
    }, headers=agent_headers)
    assert c_resp.status_code == 201

    # 6. Agent posts internal note
    note_resp = client.post(f"/api/v1/tickets/{t_id}/comments", json={
        "content": "Internal agent note: root cause identified",
        "is_internal_note": True
    }, headers=agent_headers)
    assert note_resp.status_code == 201

    # 7. Agent resolves ticket
    res_resp = client.put(f"/api/v1/tickets/{t_id}/status", json={
        "status": "RESOLVED",
        "reason": "Fixed root cause"
    }, headers=agent_headers)
    assert res_resp.status_code == 200
    assert res_resp.json()["status"] == "RESOLVED"

    # 8. Employee views ticket and closes it
    close_resp = client.put(f"/api/v1/tickets/{t_id}/status", json={
        "status": "CLOSED"
    }, headers=emp_headers)
    assert close_resp.status_code == 200
    assert close_resp.json()["status"] == "CLOSED"
