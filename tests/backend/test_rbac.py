import pytest
from app.security.rbac import ROLE_PERMISSIONS

def test_role_permissions_matrix():
    assert "ticket.create" in ROLE_PERMISSIONS["EMPLOYEE"]
    assert "ticket.assign" in ROLE_PERMISSIONS["AGENT"]
    assert "reports.view" in ROLE_PERMISSIONS["MANAGER"]
    assert "audit.view" in ROLE_PERMISSIONS["ADMIN"]

def test_unauthenticated_request_blocked(client):
    response = client.get("/api/v1/users")
    assert response.status_code == 401
