import pytest

def test_add_public_comment(client):
    emp_login = client.post("/api/v1/auth/login", json={
        "email": "employee.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = emp_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    t_resp = client.post("/api/v1/tickets", json={
        "title": "Software license error",
        "description": "IntelliJ license key expired",
        "category_id": 1,
        "priority": "LOW"
    }, headers=headers)
    t_id = t_resp.json()["id"]

    comment_resp = client.post(f"/api/v1/tickets/{t_id}/comments", json={
        "content": "I have uploaded the screenshot for reference.",
        "is_internal_note": False
    }, headers=headers)
    assert comment_resp.status_code == 201
    assert comment_resp.json()["content"] == "I have uploaded the screenshot for reference."
