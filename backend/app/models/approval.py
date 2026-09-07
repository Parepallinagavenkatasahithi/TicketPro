from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    title = Column(String(200), nullable=False)
    rationale = Column(Text, nullable=True)
    status = Column(String(30), nullable=False, default=ApprovalStatus.PENDING.value, index=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    ticket = relationship("Ticket", back_populates="approvals")
    requester = relationship("User", foreign_keys=[requester_id])
    steps = relationship("ApprovalStep", back_populates="approval_request", cascade="all, delete-orphan")


class ApprovalStep(Base):
    __tablename__ = "approval_steps"

    id = Column(Integer, primary_key=True, index=True)
    approval_request_id = Column(Integer, ForeignKey("approval_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    step_number = Column(Integer, default=1)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    status = Column(String(30), nullable=False, default=ApprovalStatus.PENDING.value)
    decision_notes = Column(Text, nullable=True)
    decided_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    approval_request = relationship("ApprovalRequest", back_populates="steps")
    approver = relationship("User", foreign_keys=[approver_id])
