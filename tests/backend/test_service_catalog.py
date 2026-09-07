import pytest
from fastapi.testclient import TestClient

def test_service_catalog_categories_and_items(client: TestClient, admin_token_headers: dict):
    # 1. Category
    c_res = client.post("/api/v1/service-catalog/categories", json={
        "name": "Hardware Provisioning",
        "description": "Request laptops, monitors, and peripherals",
        "icon_name": "Laptop"
    }, headers=admin_token_headers)
    assert c_res.status_code == 201
    cat = c_res.json()

    # 2. Item
    i_res = client.post("/api/v1/service-catalog/items", json={
        "category_id": cat["id"],
        "name": "Developer Workstation Pro",
        "short_description": "Apple MacBook Pro 16 or Dell XPS 15",
        "estimated_fulfillment_hours": 48.0,
        "requires_approval": True,
        "cost": 2500.0
    }, headers=admin_token_headers)
    assert i_res.status_code == 201
    item = i_res.json()
    assert item["name"] == "Developer Workstation Pro"

    # 3. List
    cats_list = client.get("/api/v1/service-catalog/categories", headers=admin_token_headers)
    assert cats_list.status_code == 200
    items_list = client.get("/api/v1/service-catalog/items", headers=admin_token_headers)
    assert items_list.status_code == 200
    assert len(items_list.json()) >= 1
