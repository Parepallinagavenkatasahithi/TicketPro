from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sla import SLAPolicy, SLABreach
from app.models.ticket import Ticket, TicketStatus
from app.schemas.sla import SLAPolicyCreate, SLAPolicyUpdate
from app.domain.sla_calculator import check_sla_status
from app.core.exceptions import NotFoundError, ValidationError


class SLAService:
    def __init__(self, db: Session):
        self.db = db

    def get_policies(self) -> List[SLAPolicy]:
        return self.db.query(SLAPolicy).filter(SLAPolicy.is_active == True).all()

    def get_policy_by_id(self, policy_id: int) -> SLAPolicy:
        policy = self.db.query(SLAPolicy).filter(SLAPolicy.id == policy_id).first()
        if not policy:
            raise NotFoundError("SLA Policy", str(policy_id))
        return policy

    def create_policy(self, policy_in: SLAPolicyCreate) -> SLAPolicy:
        existing = self.db.query(SLAPolicy).filter(SLAPolicy.priority == policy_in.priority).first()
        if existing:
            raise ValidationError(f"SLA policy for priority '{policy_in.priority}' already exists")

        policy = SLAPolicy(
            name=policy_in.name,
            description=policy_in.description,
            priority=policy_in.priority,
            max_first_response_minutes=policy_in.max_first_response_minutes,
            max_resolution_minutes=policy_in.max_resolution_minutes,
            warning_threshold_percent=policy_in.warning_threshold_percent,
            is_default=policy_in.is_default,
            is_active=True
        )
        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)
        return policy

    def evaluate_all_active_tickets_sla(self) -> int:
        """Scan active tickets and flag SLA breaches."""
        active_tickets = self.db.query(Ticket).filter(
            Ticket.status.notin_([TicketStatus.RESOLVED.value, TicketStatus.CLOSED.value, TicketStatus.CANCELLED.value])
        ).all()

        breach_count = 0
        now = datetime.now(timezone.utc)

        for ticket in active_tickets:
            sla_check = check_sla_status(
                ticket.created_at,
                ticket.first_response_due_at,
                ticket.first_responded_at,
                ticket.resolution_due_at,
                ticket.resolved_at
            )

            # Update breach fields
            if sla_check["first_response_breached"] and not ticket.first_response_breached:
                ticket.first_response_breached = True
                breach = SLABreach(
                    ticket_id=ticket.id,
                    breach_type="FIRST_RESPONSE",
                    agent_id=ticket.assigned_agent_id,
                    expected_at=ticket.first_response_due_at,
                    actual_at=None,
                    reason="First response time limit exceeded"
                )
                self.db.add(breach)
                breach_count += 1

            if sla_check["resolution_breached"] and not ticket.resolution_breached:
                ticket.resolution_breached = True
                breach = SLABreach(
                    ticket_id=ticket.id,
                    breach_type="RESOLUTION",
                    agent_id=ticket.assigned_agent_id,
                    expected_at=ticket.resolution_due_at,
                    actual_at=None,
                    reason="Resolution time limit exceeded"
                )
                self.db.add(breach)
                breach_count += 1

            ticket.is_overdue = sla_check["is_overdue"]

        self.db.commit()
        return breach_count
