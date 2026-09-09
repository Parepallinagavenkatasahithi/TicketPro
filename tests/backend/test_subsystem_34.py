import pytest
from backend.app.domain.security_posture.module_1 import SecurityPostureServiceModule1
from backend.app.domain.security_posture.module_2 import SecurityPostureServiceModule2
from backend.app.domain.security_posture.module_3 import SecurityPostureServiceModule3

def test_subsystem_34_module1_execution():
    service = SecurityPostureServiceModule1(service_id=34)
    assert service.service_id == 34
    assert service.subsystem_name == "security_posture"
    
    res = service.process_subsystem_transaction_1(
        transaction_id="TX-TEST-34-01",
        entity_id=134,
        payload={"title": "Test Ticket", "category": "IT"},
        actor_id=1
    )
    assert res["success"] is True
    assert res["status_code"] == 200
    assert res["audit_record"]["subsystem"] == "security_posture"
    assert "metrics" in res
    assert res["metrics"]["efficiency_score"] > 0

def test_subsystem_34_access_control():
    service = SecurityPostureServiceModule2(service_id=34)
    auth_res = service.validate_access_policy_2(
        user_role="ADMIN",
        required_permission="write",
        tenant_id="tenant-alpha"
    )
    assert auth_res["authorized"] is True

def test_subsystem_34_export_transformation():
    service = SecurityPostureServiceModule3(service_id=34)
    records = [
        {"id": 1, "title": "Item A", "status": "active", "score": 95.0},
        {"id": 2, "title": "Item B", "status": "pending", "score": 88.0}
    ]
    export_res = service.format_export_dataset_3(records)
    assert export_res["total_count"] == 2
    assert len(export_res["records"]) == 2
    assert export_res["records"][0]["summary"] == "Item A"
