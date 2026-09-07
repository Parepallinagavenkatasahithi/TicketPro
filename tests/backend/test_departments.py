import pytest

def test_get_departments(client):
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = login_resp.json()["access_token"]
    
    response = client.get("/api/v1/departments", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    depts = response.json()
    assert any(d["code"] == "IT" for d in depts)
