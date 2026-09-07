from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.models.ticket import TicketStatus, TicketPriority


class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    default_priority: str
    default_department_id: Optional[int] = None
    icon_name: Optional[str] = "HelpCircle"
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    default_priority: str = "MEDIUM"
    default_department_id: Optional[int] = None
    icon_name: Optional[str] = "HelpCircle"


class TicketCreate(BaseModel):
    title: str
    description: str
    category_id: int
    priority: TicketPriority = TicketPriority.MEDIUM
    department_id: Optional[int] = None
    contact_method: str = "EMAIL"


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    priority: Optional[TicketPriority] = None
    department_id: Optional[int] = None


class TicketStatusUpdate(BaseModel):
    status: TicketStatus
    reason: Optional[str] = None


class TicketPriorityUpdate(BaseModel):
    priority: TicketPriority
    reason: Optional[str] = None


class TicketAssignRequest(BaseModel):
    agent_id: int
    reason: Optional[str] = None


class TicketOut(BaseModel):
    id: int
    ticket_number: str
    title: str
    description: str
    category_id: int
    category_name: Optional[str] = None
    priority: str
    status: str
    
    requester_id: int
    requester_name: Optional[str] = None
    requester_email: Optional[str] = None
    
    assigned_agent_id: Optional[int] = None
    assigned_agent_name: Optional[str] = None
    
    department_id: int
    department_name: Optional[str] = None
    
    sla_policy_id: Optional[int] = None
    first_response_due_at: Optional[datetime] = None
    first_responded_at: Optional[datetime] = None
    first_response_breached: bool = False
    
    resolution_due_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_breached: bool = False
    closed_at: Optional[datetime] = None
    is_overdue: bool = False
    
    contact_method: str = "EMAIL"
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketHistoryOut(BaseModel):
    id: int
    actor_id: int
    actor_name: Optional[str] = None
    event_type: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketDetail(TicketOut):
    comments: List["CommentOut"] = []
    attachments: List["AttachmentOut"] = []
    history: List[TicketHistoryOut] = []

    model_config = ConfigDict(from_attributes=True)


from app.schemas.comment import CommentOut  # noqa
from app.schemas.attachment import AttachmentOut  # noqa
TicketDetail.model_rebuild()
