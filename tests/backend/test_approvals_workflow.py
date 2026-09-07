import pytest

def test_approval_workflow_lifecycle(client):
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create ticket
    t_resp = client.post("/api/v1/tickets", json={
        "title": "AWS Admin Access Request",
        "description": "Requesting production admin access",
        "category_id": 1,
        "priority": "HIGH"
    }, headers=headers)
    t_id = t_resp.json()["id"]

    # Request approval
    app_resp = client.post("/api/v1/approvals", json={
        "ticket_id": t_id,
        "title": "AWS Admin Privilege Approval",
        "rationale": "Required for release",
        "approver_ids": [1]
    }, headers=headers)
    assert app_resp.status_code == 201
    app_data = app_resp.json()
    assert app_data["status"] == "PENDING"
    step_id = app_data["steps"][0]["id"]

    # Approve step
    decide_resp = client.put(f"/api/v1/approvals/steps/{step_id}/decide", json={
        "decision": "APPROVED",
        "notes": "Approved for release deployment"
    }, headers=headers)
    assert decide_resp.status_code == 200
    assert decide_resp.json()["status"] == "APPROVED"
