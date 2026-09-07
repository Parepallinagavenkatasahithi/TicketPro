import pytest
from fastapi.testclient import TestClient

def test_custom_fields_creation_and_values(client: TestClient, admin_token_headers: dict):
    # 1. Create custom field
    cf_res = client.post("/api/v1/custom-fields", json={
        "name": "Cost Center Code",
        "field_key": "cost_center_code",
        "field_type": "TEXT",
        "target_entity": "TICKET",
        "is_required": True
    }, headers=admin_token_headers)
    assert cf_res.status_code == 201
    cf = cf_res.json()
    assert cf["field_key"] == "cost_center_code"

    # 2. Set value
    v_res = client.post("/api/v1/custom-fields/values", json={
        "custom_field_id": cf["id"],
        "entity_id": 101,
        "field_value": "CC-9042-ENG"
    }, headers=admin_token_headers)
    assert v_res.status_code == 201

    # 3. List fields
    list_res = client.get("/api/v1/custom-fields?target_entity=TICKET", headers=admin_token_headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1
