from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class TimeEntry(Base):
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hours_spent = Column(Float, nullable=False)
    activity_type = Column(String(50), default="RESEARCH") # RESEARCH, TROUBLESHOOTING, COMMUNICATION, REPAIR, DEPLOYMENT
    description = Column(Text, nullable=True)
    
    logged_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    ticket = relationship("Ticket")
    user = relationship("User")
