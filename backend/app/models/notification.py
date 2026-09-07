from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    
    notification_type = Column(String(50), nullable=False)  # TICKET_ASSIGNED, TICKET_UPDATED, TICKET_COMMENT, SLA_WARNING, SLA_BREACH, APPROVAL_REQUIRED, ANNOUNCEMENT
    reference_id = Column(String(100), nullable=True)     # ticket_number or announcement id
    
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User")
