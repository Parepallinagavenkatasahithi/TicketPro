from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sla import EscalationPolicy, EscalationEvent
from app.models.ticket import Ticket, TicketPriority, TicketHistory
from app.models.user import User
from app.services.notification_service import NotificationService
from app.core.exceptions import NotFoundError


class EscalationService:
    def __init__(self, db: Session):
        self.db = db

    def escalate_ticket(
        self,
        ticket_id: int,
        triggered_by: Optional[User] = None,
        reason: str = "Automatic SLA Breach Escalation"
    ) -> EscalationEvent:
        ticket = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise NotFoundError("Ticket", str(ticket_id))

        old_priority = ticket.priority
        new_priority = old_priority

        # Priority bump logic: LOW -> MEDIUM -> HIGH -> CRITICAL
        priority_map = {
            "LOW": "MEDIUM",
            "MEDIUM": "HIGH",
            "HIGH": "CRITICAL",
            "CRITICAL": "CRITICAL"
        }
        new_priority = priority_map.get(old_priority, "HIGH")
        ticket.priority = new_priority
        ticket.is_overdue = True

        # Find manager to notify
        manager = self.db.query(User).filter(
            User.department_id == ticket.department_id,
            User.role_name == "MANAGER"
        ).first()

        event = EscalationEvent(
            ticket_id=ticket.id,
            triggered_by_id=triggered_by.id if triggered_by else None,
            old_priority=old_priority,
            new_priority=new_priority,
            notified_user_id=manager.id if manager else None,
            notes=reason,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(event)

        # Log ticket history
        history = TicketHistory(
            ticket_id=ticket.id,
            actor_id=triggered_by.id if triggered_by else (manager.id if manager else ticket.requester_id),
            event_type="ESCALATED",
            old_value=old_priority,
            new_value=new_priority,
            description=f"Escalated due to: {reason}. Priority bumped to {new_priority}."
        )
        self.db.add(history)

        # Trigger notification
        if manager:
            notif_service = NotificationService(self.db)
            notif_service.create_notification(
                user_id=manager.id,
                title=f"ESCALATION ALERT: {ticket.ticket_number}",
                message=f"Ticket '{ticket.title}' has been escalated to {new_priority} priority. Reason: {reason}",
                notification_type="SLA_BREACH",
                reference_id=ticket.ticket_number
            )

        self.db.commit()
        self.db.refresh(event)
        return event
