import pytest

def test_process_time_header_present(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert "x-process-time" in resp.headers
