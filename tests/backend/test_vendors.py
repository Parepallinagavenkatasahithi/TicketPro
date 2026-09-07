import pytest
from fastapi.testclient import TestClient

def test_list_and_create_vendors(client: TestClient, admin_token_headers: dict):
    # 1. Create Vendor
    v_data = {
        "name": "Datadog Monitoring Inc.",
        "code": "DATADOG",
        "contact_name": "Sarah Connor",
        "contact_email": "sarah.connor@datadog.com",
        "website": "https://datadoghq.com",
        "rating": 4.9
    }
    res = client.post("/api/v1/vendors", json=v_data, headers=admin_token_headers)
    assert res.status_code == 201
    v = res.json()
    assert v["name"] == v_data["name"]

    # 2. List Vendors
    list_res = client.get("/api/v1/vendors", headers=admin_token_headers)
    assert list_res.status_code == 200
    vendors = list_res.json()
    assert len(vendors) >= 1

    # 3. Create License
    lic_data = {
        "vendor_id": v["id"],
        "software_name": "Datadog APM Enterprise",
        "license_type": "PER_USER",
        "total_seats": 50,
        "cost_per_seat": 150.0
    }
    lic_res = client.post("/api/v1/vendors/licenses", json=lic_data, headers=admin_token_headers)
    assert lic_res.status_code == 201
    lic = lic_res.json()
    assert lic["software_name"] == lic_data["software_name"]

    # 4. List Licenses
    lic_list = client.get("/api/v1/vendors/licenses", headers=admin_token_headers)
    assert lic_list.status_code == 200
    assert len(lic_list.json()) >= 1
