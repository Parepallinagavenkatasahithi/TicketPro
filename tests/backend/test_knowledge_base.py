import pytest

def test_kb_article_create_and_search(client):
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = client.post("/api/v1/knowledge-base", json={
        "title": "VPN Setup Guide",
        "content": "Follow these steps to setup WireGuard VPN",
        "category_id": 1,
        "status": "PUBLISHED",
        "tags": "vpn,network"
    }, headers=headers)
    assert create_resp.status_code == 201
    article = create_resp.json()
    assert article["slug"] == "vpn-setup-guide"

    list_resp = client.get("/api/v1/knowledge-base?search=WireGuard", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1
