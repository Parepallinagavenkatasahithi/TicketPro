import pytest
from fastapi.testclient import TestClient

def test_list_and_create_change_requests(client: TestClient, admin_token_headers: dict):
    chg_data = {
        "title": "Upgrade Core Router Firmware to v4.2.1",
        "description": "Perform scheduled firmware patch during maintenance window.",
        "reason_for_change": "Fix security vulnerability CVE-2026-1029",
        "impact_analysis": "30 minutes downtime for network switch stack B.",
        "rollback_plan": "Restore backup image via TFTP server.",
        "category": "INFRASTRUCTURE",
        "risk_level": "MEDIUM"
    }
    res = client.post("/api/v1/change-requests", json=chg_data, headers=admin_token_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == chg_data["title"]
    assert data["status"] == "PENDING_APPROVAL"

    list_res = client.get("/api/v1/change-requests", headers=admin_token_headers)
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) >= 1
    assert any(c["title"] == chg_data["title"] for c in items)
