import pytest
from fastapi.testclient import TestClient

def test_list_and_create_assets(client: TestClient, admin_token_headers: dict):
    # 1. Create asset
    asset_data = {
        "asset_tag": "AST-TEST-99",
        "name": "MacBook Pro 16 M3 Max",
        "category": "HARDWARE",
        "model_number": "MBP-16-2024",
        "serial_number": "SN123456789",
        "status": "IN_USE",
        "location": "Headquarters 4F",
        "purchase_cost": 3499.00,
        "vendor_name": "Apple Inc."
    }
    response = client.post("/api/v1/assets", json=asset_data, headers=admin_token_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["asset_tag"] == "AST-TEST-99"
    assert data["name"] == "MacBook Pro 16 M3 Max"

    # 2. List assets
    list_res = client.get("/api/v1/assets", headers=admin_token_headers)
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) >= 1
    assert any(a["asset_tag"] == "AST-TEST-99" for a in items)
