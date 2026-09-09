import pytest
from backend.app.domain.search_engine.module_1 import SearchEngineServiceModule1
from backend.app.domain.search_engine.module_2 import SearchEngineServiceModule2
from backend.app.domain.search_engine.module_3 import SearchEngineServiceModule3

def test_subsystem_18_module1_execution():
    service = SearchEngineServiceModule1(service_id=18)
    assert service.service_id == 18
    assert service.subsystem_name == "search_engine"
    
    res = service.process_subsystem_transaction_1(
        transaction_id="TX-TEST-18-01",
        entity_id=118,
        payload={"title": "Test Ticket", "category": "IT"},
        actor_id=1
    )
    assert res["success"] is True
    assert res["status_code"] == 200
    assert res["audit_record"]["subsystem"] == "search_engine"
    assert "metrics" in res
    assert res["metrics"]["efficiency_score"] > 0

def test_subsystem_18_access_control():
    service = SearchEngineServiceModule2(service_id=18)
    auth_res = service.validate_access_policy_2(
        user_role="ADMIN",
        required_permission="write",
        tenant_id="tenant-alpha"
    )
    assert auth_res["authorized"] is True

def test_subsystem_18_export_transformation():
    service = SearchEngineServiceModule3(service_id=18)
    records = [
        {"id": 1, "title": "Item A", "status": "active", "score": 95.0},
        {"id": 2, "title": "Item B", "status": "pending", "score": 88.0}
    ]
    export_res = service.format_export_dataset_3(records)
    assert export_res["total_count"] == 2
    assert len(export_res["records"]) == 2
    assert export_res["records"][0]["summary"] == "Item A"
