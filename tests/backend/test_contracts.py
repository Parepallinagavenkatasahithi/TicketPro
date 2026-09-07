import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

def test_list_and_create_contracts(client: TestClient, admin_token_headers: dict):
    # First create a vendor
    v_res = client.post("/api/v1/vendors", json={
        "name": "AWS Cloud Services",
        "code": "AWS-CLD"
    }, headers=admin_token_headers)
    v_id = v_res.json()["id"]

    c_data = {
        "contract_number": "CNT-2026-901",
        "title": "AWS Enterprise Support Contract",
        "vendor_id": v_id,
        "contract_type": "CLOUD_SERVICE",
        "status": "ACTIVE",
        "annual_cost": 45000.0,
        "start_date": "2026-01-01T00:00:00Z",
        "end_date": "2027-01-01T00:00:00Z",
        "auto_renew": True
    }
    c_res = client.post("/api/v1/contracts", json=c_data, headers=admin_token_headers)
    assert c_res.status_code == 201
    contract = c_res.json()
    assert contract["contract_number"] == c_data["contract_number"]

    list_res = client.get("/api/v1/contracts", headers=admin_token_headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1
