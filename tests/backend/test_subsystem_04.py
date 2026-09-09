import pytest
from backend.app.domain.intelligent_routing.module_1 import IntelligentRoutingServiceModule1
from backend.app.domain.intelligent_routing.module_2 import IntelligentRoutingServiceModule2
from backend.app.domain.intelligent_routing.module_3 import IntelligentRoutingServiceModule3

def test_subsystem_4_module1_execution():
    service = IntelligentRoutingServiceModule1(service_id=4)
    assert service.service_id == 4
    assert service.subsystem_name == "intelligent_routing"
    
    res = service.process_subsystem_transaction_1(
        transaction_id="TX-TEST-4-01",
        entity_id=104,
        payload={"title": "Test Ticket", "category": "IT"},
        actor_id=1
    )
    assert res["success"] is True
    assert res["status_code"] == 200
    assert res["audit_record"]["subsystem"] == "intelligent_routing"
    assert "metrics" in res
    assert res["metrics"]["efficiency_score"] > 0

def test_subsystem_4_access_control():
    service = IntelligentRoutingServiceModule2(service_id=4)
    auth_res = service.validate_access_policy_2(
        user_role="ADMIN",
        required_permission="write",
        tenant_id="tenant-alpha"
    )
    assert auth_res["authorized"] is True

def test_subsystem_4_export_transformation():
    service = IntelligentRoutingServiceModule3(service_id=4)
    records = [
        {"id": 1, "title": "Item A", "status": "active", "score": 95.0},
        {"id": 2, "title": "Item B", "status": "pending", "score": 88.0}
    ]
    export_res = service.format_export_dataset_3(records)
    assert export_res["total_count"] == 2
    assert len(export_res["records"]) == 2
    assert export_res["records"][0]["summary"] == "Item A"
