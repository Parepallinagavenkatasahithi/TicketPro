from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class TicketStatus(str, enum.Enum):
    NEW = "NEW"
    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_FOR_USER = "WAITING_FOR_USER"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    REOPENED = "REOPENED"
    CANCELLED = "CANCELLED"


class TicketPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TicketCategory(Base):
    __tablename__ = "ticket_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)  # Hardware, Software, Network, etc.
    description = Column(Text, nullable=True)
    default_priority = Column(String(20), default=TicketPriority.MEDIUM.value)
    default_department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    icon_name = Column(String(50), nullable=True, default="HelpCircle")
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    tickets = relationship("Ticket", back_populates="category")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(50), unique=True, nullable=False, index=True)  # TKT-YYYY-NNNN
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    category_id = Column(Integer, ForeignKey("ticket_categories.id"), nullable=False)
    priority = Column(String(20), nullable=False, default=TicketPriority.MEDIUM.value, index=True)
    status = Column(String(30), nullable=False, default=TicketStatus.NEW.value, index=True)
    
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    assigned_agent_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    sla_policy_id = Column(Integer, ForeignKey("sla_policies.id"), nullable=True)
    
    contact_method = Column(String(50), default="EMAIL")
    
    # SLA Tracking
    first_response_due_at = Column(DateTime(timezone=True), nullable=True)
    first_responded_at = Column(DateTime(timezone=True), nullable=True)
    first_response_breached = Column(Boolean, default=False)
    
    resolution_due_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolution_breached = Column(Boolean, default=False)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    is_overdue = Column(Boolean, default=False, index=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    category = relationship("TicketCategory", back_populates="tickets")
    requester = relationship("User", foreign_keys=[requester_id], back_populates="requested_tickets")
    assigned_agent = relationship("User", foreign_keys=[assigned_agent_id], back_populates="assigned_tickets")
    department = relationship("Department", back_populates="tickets")
    sla_policy = relationship("SLAPolicy", back_populates="tickets")
    
    comments = relationship("TicketComment", back_populates="ticket", cascade="all, delete-orphan")
    attachments = relationship("TicketAttachment", back_populates="ticket", cascade="all, delete-orphan")
    history = relationship("TicketHistory", back_populates="ticket", cascade="all, delete-orphan")
    assignments = relationship("TicketAssignment", back_populates="ticket", cascade="all, delete-orphan")
    approvals = relationship("ApprovalRequest", back_populates="ticket", cascade="all, delete-orphan")


class TicketComment(Base):
    __tablename__ = "ticket_comments"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_internal_note = Column(Boolean, default=False, nullable=False, index=True)  # True = agent only
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    ticket = relationship("Ticket", back_populates="comments")
    author = relationship("User", back_populates="comments")
    attachments = relationship("TicketAttachment", back_populates="comment")


class TicketAttachment(Base):
    __tablename__ = "ticket_attachments"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    comment_id = Column(Integer, ForeignKey("ticket_comments.id", ondelete="SET NULL"), nullable=True)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    file_name = Column(String(255), nullable=False)
    storage_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    mime_type = Column(String(100), nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    ticket = relationship("Ticket", back_populates="attachments")
    comment = relationship("TicketComment", back_populates="attachments")
    uploader = relationship("User")


class TicketHistory(Base):
    __tablename__ = "ticket_history"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_type = Column(String(50), nullable=False)  # CREATED, STATUS_CHANGED, PRIORITY_CHANGED, ASSIGNED, COMMENT_ADDED, ESCALATED, RESOLVED, REOPENED
    old_value = Column(String(255), nullable=True)
    new_value = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    ticket = relationship("Ticket", back_populates="history")
    actor = relationship("User")


class TicketAssignment(Base):
    __tablename__ = "ticket_assignments"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason = Column(String(255), nullable=True)
    
    assigned_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    ticket = relationship("Ticket", back_populates="assignments")
    agent = relationship("User", foreign_keys=[agent_id])
    assigned_by = relationship("User", foreign_keys=[assigned_by_id])
