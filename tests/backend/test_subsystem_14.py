import pytest
from backend.app.domain.incident_response.module_1 import IncidentResponseServiceModule1
from backend.app.domain.incident_response.module_2 import IncidentResponseServiceModule2
from backend.app.domain.incident_response.module_3 import IncidentResponseServiceModule3

def test_subsystem_14_module1_execution():
    service = IncidentResponseServiceModule1(service_id=14)
    assert service.service_id == 14
    assert service.subsystem_name == "incident_response"
    
    res = service.process_subsystem_transaction_1(
        transaction_id="TX-TEST-14-01",
        entity_id=114,
        payload={"title": "Test Ticket", "category": "IT"},
        actor_id=1
    )
    assert res["success"] is True
    assert res["status_code"] == 200
    assert res["audit_record"]["subsystem"] == "incident_response"
    assert "metrics" in res
    assert res["metrics"]["efficiency_score"] > 0

def test_subsystem_14_access_control():
    service = IncidentResponseServiceModule2(service_id=14)
    auth_res = service.validate_access_policy_2(
        user_role="ADMIN",
        required_permission="write",
        tenant_id="tenant-alpha"
    )
    assert auth_res["authorized"] is True

def test_subsystem_14_export_transformation():
    service = IncidentResponseServiceModule3(service_id=14)
    records = [
        {"id": 1, "title": "Item A", "status": "active", "score": 95.0},
        {"id": 2, "title": "Item B", "status": "pending", "score": 88.0}
    ]
    export_res = service.format_export_dataset_3(records)
    assert export_res["total_count"] == 2
    assert len(export_res["records"]) == 2
    assert export_res["records"][0]["summary"] == "Item A"
