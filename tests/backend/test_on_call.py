import pytest
from fastapi.testclient import TestClient

def test_list_and_create_on_call_rotations(client: TestClient, admin_token_headers: dict):
    rot_data = {
        "name": "DevOps Primary On-Call",
        "department_id": 1,
        "rotation_type": "WEEKLY",
        "start_time": "08:00",
        "time_zone": "UTC"
    }
    r_res = client.post("/api/v1/on-call", json=rot_data, headers=admin_token_headers)
    assert r_res.status_code == 201
    rot = r_res.json()
    assert rot["name"] == rot_data["name"]

    shift_data = {
        "rotation_id": rot["id"],
        "user_id": 1,
        "start_at": "2026-09-01T00:00:00Z",
        "end_at": "2026-09-08T00:00:00Z"
    }
    s_res = client.post("/api/v1/on-call/shifts", json=shift_data, headers=admin_token_headers)
    assert s_res.status_code == 201

    list_res = client.get("/api/v1/on-call", headers=admin_token_headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1
