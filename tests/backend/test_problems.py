import pytest
from fastapi.testclient import TestClient

def test_list_and_create_problems(client: TestClient, admin_token_headers: dict):
    prb_data = {
        "title": "Intermittent Database Connection Dropouts",
        "description": "High latency spike triggers connection pool exhaustion every 4 hours.",
        "impact": "HIGH",
        "root_cause": "Unindexed full table scan on audit logs under heavy load.",
        "workaround": "Restart web worker pool to release stale connections."
    }
    res = client.post("/api/v1/problems", json=prb_data, headers=admin_token_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == prb_data["title"]
    assert data["status"] == "INVESTIGATING"

    list_res = client.get("/api/v1/problems", headers=admin_token_headers)
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) >= 1
    assert any(p["title"] == prb_data["title"] for p in items)
