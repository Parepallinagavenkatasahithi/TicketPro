import pytest
from backend.app.domain.change_mgmt.module_1 import ChangeMgmtServiceModule1
from backend.app.domain.change_mgmt.module_2 import ChangeMgmtServiceModule2
from backend.app.domain.change_mgmt.module_3 import ChangeMgmtServiceModule3

def test_subsystem_12_module1_execution():
    service = ChangeMgmtServiceModule1(service_id=12)
    assert service.service_id == 12
    assert service.subsystem_name == "change_mgmt"
    
    res = service.process_subsystem_transaction_1(
        transaction_id="TX-TEST-12-01",
        entity_id=112,
        payload={"title": "Test Ticket", "category": "IT"},
        actor_id=1
    )
    assert res["success"] is True
    assert res["status_code"] == 200
    assert res["audit_record"]["subsystem"] == "change_mgmt"
    assert "metrics" in res
    assert res["metrics"]["efficiency_score"] > 0

def test_subsystem_12_access_control():
    service = ChangeMgmtServiceModule2(service_id=12)
    auth_res = service.validate_access_policy_2(
        user_role="ADMIN",
        required_permission="write",
        tenant_id="tenant-alpha"
    )
    assert auth_res["authorized"] is True

def test_subsystem_12_export_transformation():
    service = ChangeMgmtServiceModule3(service_id=12)
    records = [
        {"id": 1, "title": "Item A", "status": "active", "score": 95.0},
        {"id": 2, "title": "Item B", "status": "pending", "score": 88.0}
    ]
    export_res = service.format_export_dataset_3(records)
    assert export_res["total_count"] == 2
    assert len(export_res["records"]) == 2
    assert export_res["records"][0]["summary"] == "Item A"
