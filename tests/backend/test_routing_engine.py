import pytest
from app.services.routing_service import TicketRoutingService
from app.models.ticket import Ticket, TicketStatus

def test_routing_service_assigns_available_agent(db):
    service = TicketRoutingService(db)
    ticket = Ticket(
        ticket_number="TKT-TEST-9999",
        title="Routing test ticket",
        description="Routing test desc",
        category_id=1,
        priority="MEDIUM",
        status=TicketStatus.NEW.value,
        requester_id=3,
        department_id=1
    )
    db.add(ticket)
    db.commit()

    agent = service.route_and_assign_ticket(ticket)
    assert agent is not None
    assert ticket.assigned_agent_id == agent.id
    assert ticket.status == TicketStatus.ASSIGNED.value
