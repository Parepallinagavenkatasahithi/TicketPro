from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    problem_number = Column(String(50), unique=True, nullable=False, index=True) # PRB-2026-1001
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=True)
    workaround = Column(Text, nullable=True)
    
    status = Column(String(30), default="INVESTIGATING") # LOGGED, INVESTIGATING, KNOWN_ERROR, RESOLVED, CLOSED
    impact = Column(String(20), default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = relationship("User", foreign_keys=[owner_id])
    department = relationship("Department", foreign_keys=[department_id])
