from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ticket import (
    TicketOut, TicketCreate, TicketDetail, TicketStatusUpdate,
    TicketPriorityUpdate, TicketAssignRequest, CategoryOut, CategoryCreate
)
from app.schemas.comment import CommentOut
from app.schemas.attachment import AttachmentOut
from app.models.ticket import TicketCategory, TicketComment, TicketAttachment, TicketHistory
from app.services.ticket_service import TicketService
from app.services.escalation_service import EscalationService
from app.services.audit_service import AuditService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()


@router.get("/categories", response_model=List[CategoryOut])
def get_categories(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cats = db.query(TicketCategory).filter(TicketCategory.is_active == True).all()
    return [CategoryOut.model_validate(c) for c in cats]


@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    cat_in: CategoryCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    cat = TicketCategory(
        name=cat_in.name,
        description=cat_in.description,
        default_priority=cat_in.default_priority,
        default_department_id=cat_in.default_department_id,
        icon_name=cat_in.icon_name
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return CategoryOut.model_validate(cat)


@router.get("", response_model=List[TicketOut])
def list_tickets(
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
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TicketService(db)
    tickets, total = service.list_tickets(
        current_user=current_user,
        status=status,
        priority=priority,
        category_id=category_id,
        department_id=department_id,
        assigned_agent_id=assigned_agent_id,
        requester_id=requester_id,
        search=search,
        my_tickets_only=my_tickets_only,
        is_overdue=is_overdue,
        skip=skip,
        limit=limit
    )

    results = []
    for t in tickets:
        results.append(TicketOut(
            id=t.id,
            ticket_number=t.ticket_number,
            title=t.title,
            description=t.description,
            category_id=t.category_id,
            category_name=t.category.name if t.category else None,
            priority=t.priority,
            status=t.status,
            requester_id=t.requester_id,
            requester_name=t.requester.full_name if t.requester else None,
            requester_email=t.requester.email if t.requester else None,
            assigned_agent_id=t.assigned_agent_id,
            assigned_agent_name=t.assigned_agent.full_name if t.assigned_agent else None,
            department_id=t.department_id,
            department_name=t.department.name if t.department else None,
            sla_policy_id=t.sla_policy_id,
            first_response_due_at=t.first_response_due_at,
            first_responded_at=t.first_responded_at,
            first_response_breached=t.first_response_breached,
            resolution_due_at=t.resolution_due_at,
            resolved_at=t.resolved_at,
            resolution_breached=t.resolution_breached,
            closed_at=t.closed_at,
            is_overdue=t.is_overdue,
            contact_method=t.contact_method or "EMAIL",
            created_at=t.created_at,
            updated_at=t.updated_at
        ))
    return results


@router.post("", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_in: TicketCreate,
    current_user: User = Depends(require_permission("ticket.create")),
    db: Session = Depends(get_db)
):
    service = TicketService(db)
    ticket = service.create_ticket(ticket_in, current_user)

    audit_service = AuditService(db)
    audit_service.log_event(
        action="TICKET_CREATED",
        resource_type="TICKET",
        actor_id=current_user.id,
        resource_id=ticket.ticket_number
    )

    return TicketOut(
        id=ticket.id,
        ticket_number=ticket.ticket_number,
        title=ticket.title,
        description=ticket.description,
        category_id=ticket.category_id,
        category_name=ticket.category.name if ticket.category else None,
        priority=ticket.priority,
        status=ticket.status,
        requester_id=ticket.requester_id,
        requester_name=current_user.full_name,
        requester_email=current_user.email,
        assigned_agent_id=ticket.assigned_agent_id,
        assigned_agent_name=ticket.assigned_agent.full_name if ticket.assigned_agent else None,
        department_id=ticket.department_id,
        department_name=ticket.department.name if ticket.department else None,
        sla_policy_id=ticket.sla_policy_id,
        first_response_due_at=ticket.first_response_due_at,
        resolution_due_at=ticket.resolution_due_at,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at
    )


@router.get("/{ticket_id}", response_model=TicketDetail)
def get_ticket_detail(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TicketService(db)
    t = service.get_ticket_by_id(ticket_id, current_user)

    # Filter internal notes for non-agent/admin roles (PROMPT REQUIREMENT 23, 33, 51, 73)
    comments_query = db.query(TicketComment).filter(TicketComment.ticket_id == t.id)
    if current_user.role_name == "EMPLOYEE":
        comments_query = comments_query.filter(TicketComment.is_internal_note == False)
    raw_comments = comments_query.order_by(TicketComment.created_at.asc()).all()

    formatted_comments = []
    for c in raw_comments:
        formatted_comments.append(CommentOut(
            id=c.id,
            ticket_id=c.ticket_id,
            author_id=c.author_id,
            author_name=c.author.full_name if c.author else "Unknown",
            author_role=c.author.role_name if c.author else "USER",
            author_avatar=c.author.avatar_url if c.author else None,
            content=c.content,
            is_internal_note=c.is_internal_note,
            created_at=c.created_at,
            updated_at=c.updated_at
        ))

    attachments = db.query(TicketAttachment).filter(TicketAttachment.ticket_id == t.id).all()
    formatted_attachments = [
        AttachmentOut(
            id=att.id,
            ticket_id=att.ticket_id,
            comment_id=att.comment_id,
            uploader_id=att.uploader_id,
            uploader_name=att.uploader.full_name if att.uploader else "User",
            file_name=att.file_name,
            storage_path=att.storage_path,
            file_size=att.file_size,
            mime_type=att.mime_type,
            created_at=att.created_at
        ) for att in attachments
    ]

    history_items = db.query(TicketHistory).filter(TicketHistory.ticket_id == t.id).order_by(TicketHistory.created_at.desc()).all()
    formatted_history = [
        {
            "id": h.id,
            "actor_id": h.actor_id,
            "actor_name": h.actor.full_name if h.actor else "System",
            "event_type": h.event_type,
            "old_value": h.old_value,
            "new_value": h.new_value,
            "description": h.description,
            "created_at": h.created_at
        } for h in history_items
    ]

    return TicketDetail(
        id=t.id,
        ticket_number=t.ticket_number,
        title=t.title,
        description=t.description,
        category_id=t.category_id,
        category_name=t.category.name if t.category else None,
        priority=t.priority,
        status=t.status,
        requester_id=t.requester_id,
        requester_name=t.requester.full_name if t.requester else None,
        requester_email=t.requester.email if t.requester else None,
        assigned_agent_id=t.assigned_agent_id,
        assigned_agent_name=t.assigned_agent.full_name if t.assigned_agent else None,
        department_id=t.department_id,
        department_name=t.department.name if t.department else None,
        sla_policy_id=t.sla_policy_id,
        first_response_due_at=t.first_response_due_at,
        first_responded_at=t.first_responded_at,
        first_response_breached=t.first_response_breached,
        resolution_due_at=t.resolution_due_at,
        resolved_at=t.resolved_at,
        resolution_breached=t.resolution_breached,
        closed_at=t.closed_at,
        is_overdue=t.is_overdue,
        contact_method=t.contact_method or "EMAIL",
        created_at=t.created_at,
        updated_at=t.updated_at,
        comments=formatted_comments,
        attachments=formatted_attachments,
        history=formatted_history
    )


@router.put("/{ticket_id}/status", response_model=TicketOut)
def update_status(
    ticket_id: int,
    status_in: TicketStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TicketService(db)
    ticket = service.update_status(ticket_id, status_in, current_user)
    return TicketOut.model_validate(ticket)


@router.put("/{ticket_id}/assign", response_model=TicketOut)
def assign_ticket(
    ticket_id: int,
    assign_in: TicketAssignRequest,
    current_user: User = Depends(require_permission("ticket.assign")),
    db: Session = Depends(get_db)
):
    service = TicketService(db)
    ticket = service.assign_ticket(ticket_id, assign_in.agent_id, current_user, assign_in.reason)
    return TicketOut.model_validate(ticket)


@router.post("/{ticket_id}/escalate", response_model=TicketOut)
def escalate_ticket(
    ticket_id: int,
    reason: str = "Manual Manager Escalation",
    current_user: User = Depends(require_permission("ticket.edit")),
    db: Session = Depends(get_db)
):
    escalation_service = EscalationService(db)
    escalation_service.escalate_ticket(ticket_id, current_user, reason)
    service = TicketService(db)
    ticket = service.get_ticket_by_id(ticket_id, current_user)
    return TicketOut.model_validate(ticket)
