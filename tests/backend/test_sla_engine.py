import pytest
from datetime import datetime, timedelta, timezone
from app.domain.sla_calculator import calculate_sla_due_dates, check_sla_status

def test_sla_due_dates_calculation():
    now = datetime.now(timezone.utc)
    resp_due, res_due = calculate_sla_due_dates(now, "CRITICAL")
    assert resp_due == now + timedelta(minutes=15)
    assert res_due == now + timedelta(minutes=120)

def test_sla_breach_check():
    now = datetime.now(timezone.utc)
    past_due = now - timedelta(minutes=30)
    status = check_sla_status(now - timedelta(hours=2), past_due, None, past_due, None)
    assert status["first_response_breached"] is True
    assert status["is_overdue"] is True
