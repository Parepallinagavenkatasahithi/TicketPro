import pytest
from backend.app.domain.capacity_planning.module_1 import CapacityPlanningServiceModule1
from backend.app.domain.capacity_planning.module_2 import CapacityPlanningServiceModule2
from backend.app.domain.capacity_planning.module_3 import CapacityPlanningServiceModule3

def test_subsystem_38_module1_execution():
    service = CapacityPlanningServiceModule1(service_id=38)
    assert service.service_id == 38
    assert service.subsystem_name == "capacity_planning"
    
    res = service.process_subsystem_transaction_1(
        transaction_id="TX-TEST-38-01",
        entity_id=138,
        payload={"title": "Test Ticket", "category": "IT"},
        actor_id=1
    )
    assert res["success"] is True
    assert res["status_code"] == 200
    assert res["audit_record"]["subsystem"] == "capacity_planning"
    assert "metrics" in res
    assert res["metrics"]["efficiency_score"] > 0

def test_subsystem_38_access_control():
    service = CapacityPlanningServiceModule2(service_id=38)
    auth_res = service.validate_access_policy_2(
        user_role="ADMIN",
        required_permission="write",
        tenant_id="tenant-alpha"
    )
    assert auth_res["authorized"] is True

def test_subsystem_38_export_transformation():
    service = CapacityPlanningServiceModule3(service_id=38)
    records = [
        {"id": 1, "title": "Item A", "status": "active", "score": 95.0},
        {"id": 2, "title": "Item B", "status": "pending", "score": 88.0}
    ]
    export_res = service.format_export_dataset_3(records)
    assert export_res["total_count"] == 2
    assert len(export_res["records"]) == 2
    assert export_res["records"][0]["summary"] == "Item A"
