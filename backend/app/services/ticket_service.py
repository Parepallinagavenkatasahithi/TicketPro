from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_

from app.models.ticket import (
    Ticket, TicketCategory, TicketComment, TicketAttachment,
    TicketHistory, TicketAssignment, TicketStatus, TicketPriority
)
from app.models.user import User
from app.models.sla import SLAPolicy, SLABreach
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketStatusUpdate, TicketPriorityUpdate
from app.domain.state_machine import validate_transition
from app.domain.sla_calculator import calculate_sla_due_dates, check_sla_status
from app.services.routing_service import TicketRoutingService
from app.core.exceptions import NotFoundError, PermissionDeniedError, ValidationError


class TicketService:
    def __init__(self, db: Session):
        self.db = db

    def generate_ticket_number(self) -> str:
        year = datetime.now(timezone.utc).year
        count = self.db.query(Ticket).count() + 1
        return f"TKT-{year}-{1000 + count}"

    def create_ticket(self, ticket_in: TicketCreate, requester: User) -> Ticket:
        category = self.db.query(TicketCategory).filter(TicketCategory.id == ticket_in.category_id).first()
        if not category:
            raise NotFoundError("Category", str(ticket_in.category_id))

        department_id = ticket_in.department_id or category.default_department_id or requester.department_id or 1
        ticket_num = self.generate_ticket_number()

        # Find matching SLA policy
        sla_policy = self.db.query(SLAPolicy).filter(
            SLAPolicy.priority == ticket_in.priority.value,
            SLAPolicy.is_active == True
        ).first()

        now = datetime.now(timezone.utc)
        first_resp_due, res_due = calculate_sla_due_dates(now, ticket_in.priority.value, sla_policy)

        ticket = Ticket(
            ticket_number=ticket_num,
            title=ticket_in.title,
            description=ticket_in.description,
            category_id=category.id,
            priority=ticket_in.priority.value,
            status=TicketStatus.NEW.value,
            requester_id=requester.id,
            department_id=department_id,
            sla_policy_id=sla_policy.id if sla_policy else None,
            contact_method=ticket_in.contact_method,
            first_response_due_at=first_resp_due,
            resolution_due_at=res_due,
            created_at=now,
            updated_at=now
        )
        self.db.add(ticket)
        self.db.flush()

        # History log
        history = TicketHistory(
            ticket_id=ticket.id,
            actor_id=requester.id,
            event_type="CREATED",
            new_value=TicketStatus.NEW.value,
            description=f"Ticket created by {requester.full_name}"
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(ticket)

        # Auto routing to agent
        router = TicketRoutingService(self.db)
        router.route_and_assign_ticket(ticket)

        return ticket

    def list_tickets(
        self,
        current_user: User,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category_id: Optional[int] = None,
        department_id: Optional[int] = None,
        assigned_agent_id: Optional[int] = None,
        requester_id: Optional[int] = None,
        search: Optional[str] = None,
        my_tickets_only: bool = False,
        is_overdue: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Ticket], int]:
        query = self.db.query(Ticket)

        # RBAC Filtering
        if current_user.role_name == "EMPLOYEE" or my_tickets_only:
            query = query.filter(Ticket.requester_id == current_user.id)
        elif current_user.role_name == "AGENT" and not department_id:
            # Agents see assigned + department tickets
            if current_user.department_id:
                query = query.filter(
                    or_(
                        Ticket.assigned_agent_id == current_user.id,
                        Ticket.department_id == current_user.department_id
                    )
                )

        if status:
            query = query.filter(Ticket.status == status.upper())
        if priority:
            query = query.filter(Ticket.priority == priority.upper())
        if category_id:
            query = query.filter(Ticket.category_id == category_id)
        if department_id:
            query = query.filter(Ticket.department_id == department_id)
        if assigned_agent_id:
            query = query.filter(Ticket.assigned_agent_id == assigned_agent_id)
        if requester_id:
            query = query.filter(Ticket.requester_id == requester_id)
        if is_overdue is not None:
            query = query.filter(Ticket.is_overdue == is_overdue)

        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Ticket.ticket_number.ilike(pattern),
                    Ticket.title.ilike(pattern),
                    Ticket.description.ilike(pattern)
                )
            )

        total = query.count()
        tickets = query.order_by(Ticket.created_at.desc()).offset(skip).limit(limit).all()
        return tickets, total

    def get_ticket_by_id(self, ticket_id: int, current_user: User) -> Ticket:
        ticket = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise NotFoundError("Ticket", str(ticket_id))

        # Privacy / Permission check
        if current_user.role_name == "EMPLOYEE" and ticket.requester_id != current_user.id:
            raise PermissionDeniedError("You do not have permission to view this ticket")

        return ticket

    def update_status(self, ticket_id: int, status_update: TicketStatusUpdate, actor: User) -> Ticket:
        ticket = self.get_ticket_by_id(ticket_id, actor)
        validate_transition(ticket.status, status_update.status.value, actor.role_name)

        old_status = ticket.status
        new_status = status_update.status.value
        now = datetime.now(timezone.utc)

        ticket.status = new_status
        ticket.updated_at = now

        if new_status == TicketStatus.RESOLVED.value:
            ticket.resolved_at = now
        elif new_status == TicketStatus.CLOSED.value:
            ticket.closed_at = now
        elif new_status == TicketStatus.REOPENED.value:
            ticket.resolved_at = None
            ticket.closed_at = None

        history = TicketHistory(
            ticket_id=ticket.id,
            actor_id=actor.id,
            event_type="STATUS_CHANGED",
            old_value=old_status,
            new_value=new_status,
            description=status_update.reason or f"Status changed from {old_status} to {new_status}"
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def assign_ticket(self, ticket_id: int, agent_id: int, assigner: User, reason: Optional[str] = None) -> Ticket:
        ticket = self.get_ticket_by_id(ticket_id, assigner)
        agent = self.db.query(User).filter(User.id == agent_id).first()
        if not agent:
            raise NotFoundError("Agent", str(agent_id))

        old_agent_id = ticket.assigned_agent_id
        ticket.assigned_agent_id = agent.id
        if ticket.status == TicketStatus.NEW.value or ticket.status == TicketStatus.OPEN.value:
            ticket.status = TicketStatus.ASSIGNED.value

        assignment = TicketAssignment(
            ticket_id=ticket.id,
            agent_id=agent.id,
            assigned_by_id=assigner.id,
            reason=reason or "Manual Assignment"
        )
        self.db.add(assignment)

        history = TicketHistory(
            ticket_id=ticket.id,
            actor_id=assigner.id,
            event_type="ASSIGNED",
            old_value=str(old_agent_id) if old_agent_id else "Unassigned",
            new_value=agent.full_name,
            description=f"Assigned to {agent.full_name}"
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def add_comment(self, ticket_id: int, author: User, content: str, is_internal_note: bool = False) -> TicketComment:
        ticket = self.get_ticket_by_id(ticket_id, author)

        # Critical security enforcement (prompt rule 23, 51, 73):
        # Employees can NEVER add or see internal notes!
        if is_internal_note and author.role_name == "EMPLOYEE":
            raise PermissionDeniedError("Employees cannot post internal notes")

        now = datetime.now(timezone.utc)
        comment = TicketComment(
            ticket_id=ticket.id,
            author_id=author.id,
            content=content,
            is_internal_note=is_internal_note,
            created_at=now,
            updated_at=now
        )
        self.db.add(comment)

        # First response SLA tracking: if agent/manager comments publicly for the first time
        if author.role_name in ["AGENT", "MANAGER", "ADMIN"] and not is_internal_note:
            if not ticket.first_responded_at:
                ticket.first_responded_at = now

        history = TicketHistory(
            ticket_id=ticket.id,
            actor_id=author.id,
            event_type="INTERNAL_NOTE" if is_internal_note else "COMMENT_ADDED",
            description=f"{'Internal note' if is_internal_note else 'Public comment'} added by {author.full_name}"
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(comment)
        return comment
