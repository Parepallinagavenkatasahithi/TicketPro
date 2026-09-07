from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class AnnouncementPriority(str, enum.Enum):
    NORMAL = "NORMAL"
    IMPORTANT = "IMPORTANT"
    URGENT = "URGENT"


class AnnouncementStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    SCHEDULED = "SCHEDULED"
    ARCHIVED = "ARCHIVED"


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    
    priority = Column(String(20), default=AnnouncementPriority.NORMAL.value)
    target_audience = Column(String(50), default="ALL")  # ALL, EMPLOYEE, AGENT, MANAGER, department code
    status = Column(String(30), default=AnnouncementStatus.DRAFT.value, index=True)
    
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    scheduled_for = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    author = relationship("User")
