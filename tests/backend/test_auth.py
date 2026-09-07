import pytest

def test_login_success(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "admin.test@ticketpro.internal"

def test_login_invalid_password(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401

def test_register_user(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "new.user@ticketpro.internal",
        "password": "NewUserPassword123!",
        "full_name": "New Registered User",
        "job_title": "Software Developer"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new.user@ticketpro.internal"
    assert data["role_name"] == "EMPLOYEE"
