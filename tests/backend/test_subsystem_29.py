import pytest
from backend.app.domain.on_call_roster.module_1 import OnCallRosterServiceModule1
from backend.app.domain.on_call_roster.module_2 import OnCallRosterServiceModule2
from backend.app.domain.on_call_roster.module_3 import OnCallRosterServiceModule3

def test_subsystem_29_module1_execution():
    service = OnCallRosterServiceModule1(service_id=29)
    assert service.service_id == 29
    assert service.subsystem_name == "on_call_roster"
    
    res = service.process_subsystem_transaction_1(
        transaction_id="TX-TEST-29-01",
        entity_id=129,
        payload={"title": "Test Ticket", "category": "IT"},
        actor_id=1
    )
    assert res["success"] is True
    assert res["status_code"] == 200
    assert res["audit_record"]["subsystem"] == "on_call_roster"
    assert "metrics" in res
    assert res["metrics"]["efficiency_score"] > 0

def test_subsystem_29_access_control():
    service = OnCallRosterServiceModule2(service_id=29)
    auth_res = service.validate_access_policy_2(
        user_role="ADMIN",
        required_permission="write",
        tenant_id="tenant-alpha"
    )
    assert auth_res["authorized"] is True

def test_subsystem_29_export_transformation():
    service = OnCallRosterServiceModule3(service_id=29)
    records = [
        {"id": 1, "title": "Item A", "status": "active", "score": 95.0},
        {"id": 2, "title": "Item B", "status": "pending", "score": 88.0}
    ]
    export_res = service.format_export_dataset_3(records)
    assert export_res["total_count"] == 2
    assert len(export_res["records"]) == 2
    assert export_res["records"][0]["summary"] == "Item A"
