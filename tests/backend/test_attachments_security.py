import pytest
import io

def test_upload_valid_attachment(client):
    emp_login = client.post("/api/v1/auth/login", json={
        "email": "employee.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = emp_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    t_resp = client.post("/api/v1/tickets", json={
        "title": "Attachment upload test",
        "description": "Uploading error screenshot",
        "category_id": 1,
        "priority": "LOW"
    }, headers=headers)
    t_id = t_resp.json()["id"]

    file_content = b"fake image bytes data"
    file_obj = io.BytesIO(file_content)

    res = client.post(
        f"/api/v1/tickets/{t_id}/attachments",
        files={"file": ("screenshot.png", file_obj, "image/png")},
        headers=headers
    )
    assert res.status_code == 201
    assert res.json()["file_name"] == "screenshot.png"

def test_invalid_file_extension_rejected(client):
    emp_login = client.post("/api/v1/auth/login", json={
        "email": "employee.test@ticketpro.internal",
        "password": "TestPassword123!"
    })
    token = emp_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    t_resp = client.post("/api/v1/tickets", json={
        "title": "Executable upload test",
        "description": "Uploading exe file",
        "category_id": 1,
        "priority": "LOW"
    }, headers=headers)
    t_id = t_resp.json()["id"]

    file_obj = io.BytesIO(b"malicious binary data")
    res = client.post(
        f"/api/v1/tickets/{t_id}/attachments",
        files={"file": ("malware.exe", file_obj, "application/octet-stream")},
        headers=headers
    )
    assert res.status_code == 400
