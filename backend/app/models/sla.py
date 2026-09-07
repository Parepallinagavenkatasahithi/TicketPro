from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class SLAPolicy(Base):
    __tablename__ = "sla_policies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # e.g., "Critical Priority SLA"
    description = Column(Text, nullable=True)
    priority = Column(String(20), nullable=False, unique=True, index=True)  # LOW, MEDIUM, HIGH, CRITICAL
    
    max_first_response_minutes = Column(Integer, nullable=False)  # e.g., 15 for Critical, 30 for High, 120 for Medium, 480 for Low
    max_resolution_minutes = Column(Integer, nullable=False)      # e.g., 120 for Critical, 240 for High, 480 for Medium, 1440 for Low
    warning_threshold_percent = Column(Float, default=80.0)      # % of SLA time when warning triggers (e.g. 80%)
    
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    tickets = relationship("Ticket", back_populates="sla_policy")


class SLABreach(Base):
    __tablename__ = "sla_breaches"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    breach_type = Column(String(50), nullable=False)  # FIRST_RESPONSE or RESOLUTION
    agent_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    expected_at = Column(DateTime(timezone=True), nullable=False)
    actual_at = Column(DateTime(timezone=True), nullable=True)
    breached_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reason = Column(Text, nullable=True)

    ticket = relationship("Ticket")
    agent = relationship("User")


class EscalationPolicy(Base):
    __tablename__ = "escalation_policies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    trigger_event = Column(String(50), nullable=False)  # SLA_WARNING, SLA_BREACH, MANUAL
    action = Column(String(50), nullable=False)         # NOTIFY_MANAGER, BUMP_PRIORITY, REASSIGN
    target_role = Column(String(50), default="MANAGER")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class EscalationEvent(Base):
    __tablename__ = "escalation_events"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    escalation_policy_id = Column(Integer, ForeignKey("escalation_policies.id"), nullable=True)
    triggered_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    old_priority = Column(String(20), nullable=True)
    new_priority = Column(String(20), nullable=True)
    notified_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    ticket = relationship("Ticket")
    triggered_by = relationship("User", foreign_keys=[triggered_by_id])
    notified_user = relationship("User", foreign_keys=[notified_user_id])
