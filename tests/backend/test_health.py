import pytest

def test_health_endpoints(client):
    h = client.get("/health")
    assert h.status_code == 200
    assert h.json()["status"] == "healthy"

    l = client.get("/live")
    assert l.status_code == 200

    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json()["status"] in ["ready", "degraded"]
