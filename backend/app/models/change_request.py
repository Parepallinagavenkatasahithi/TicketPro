from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ChangeRequest(Base):
    __tablename__ = "change_requests"

    id = Column(Integer, primary_key=True, index=True)
    change_number = Column(String(50), unique=True, nullable=False, index=True) # CHG-2026-1001
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    reason_for_change = Column(Text, nullable=False)
    impact_analysis = Column(Text, nullable=False)
    rollback_plan = Column(Text, nullable=False)
    
    category = Column(String(50), default="STANDARD") # STANDARD, NORMAL, EMERGENCY
    risk_level = Column(String(20), default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(30), default="DRAFT") # DRAFT, PENDING_APPROVAL, APPROVED, SCHEDULED, IN_PROGRESS, COMPLETED, REJECTED, CANCELLED
    
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_cab_lead_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    scheduled_start_at = Column(DateTime(timezone=True), nullable=True)
    scheduled_end_at = Column(DateTime(timezone=True), nullable=True)
    actual_start_at = Column(DateTime(timezone=True), nullable=True)
    actual_end_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    requester = relationship("User", foreign_keys=[requester_id])
    cab_lead = relationship("User", foreign_keys=[assigned_cab_lead_id])
