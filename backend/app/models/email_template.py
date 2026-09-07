from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.core.database import Base


class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    event_trigger = Column(String(100), nullable=False) # TICKET_CREATED, TICKET_RESOLVED, APPROVAL_REQUESTED, SLA_BREACHED
    subject_template = Column(String(255), nullable=False)
    body_template = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
