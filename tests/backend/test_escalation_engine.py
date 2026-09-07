import pytest
from app.services.escalation_service import EscalationService
from app.models.ticket import Ticket, TicketStatus

def test_escalation_service_bumps_priority(db):
    ticket = Ticket(
        ticket_number="TKT-TEST-8888",
        title="Escalation test ticket",
        description="Escalation test desc",
        category_id=1,
        priority="MEDIUM",
        status=TicketStatus.OPEN.value,
        requester_id=3,
        department_id=1
    )
    db.add(ticket)
    db.commit()

    service = EscalationService(db)
    event = service.escalate_ticket(ticket.id, reason="Testing SLA Breach Auto Escalation")
    assert event.old_priority == "MEDIUM"
    assert event.new_priority == "HIGH"
    assert ticket.priority == "HIGH"
    assert ticket.is_overdue is True
