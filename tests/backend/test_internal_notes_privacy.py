import pytest

def test_employee_cannot_post_internal_note(client):
    emp_login = client.post("/api/v1/auth/login", json={
        "email": "employee.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    emp_token = emp_login.json()["access_token"]
    emp_headers = {"Authorization": f"Bearer {emp_token}"}

    # Create ticket
    t_resp = client.post("/api/v1/tickets", json={
        "title": "Access request ticket",
        "description": "Requesting access",
        "category_id": 1,
        "priority": "MEDIUM"
    }, headers=emp_headers)
    t_id = t_resp.json()["id"]

    # Try posting internal note as employee -> MUST BE REJECTED!
    res = client.post(f"/api/v1/tickets/{t_id}/comments", json={
        "content": "Secret note attempting to leak",
        "is_internal_note": True
    }, headers=emp_headers)
    assert res.status_code in [400, 403]
