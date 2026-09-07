from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)       # e.g., "TICKET_CREATED", "STATUS_CHANGED", "USER_LOGIN"
    resource_type = Column(String(50), nullable=False, index=True) # e.g., "TICKET", "USER", "DEPARTMENT", "SLA"
    resource_id = Column(String(100), nullable=True, index=True)   # e.g., TKT-2026-1001 or user id
    
    changes_json = Column(Text, nullable=True)                     # Serialized JSON diff/payload
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    actor = relationship("User", back_populates="audit_logs")
