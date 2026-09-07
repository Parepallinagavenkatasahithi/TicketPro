from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)  # IT, HR, Finance, etc.
    code = Column(String(20), unique=True, nullable=False, index=True)  # IT, HR, FIN, ENG, OPS, FAC, SEC
    description = Column(Text, nullable=True)
    manager_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    manager = relationship("User", foreign_keys=[manager_id])
    members = relationship("User", foreign_keys="[User.department_id]", back_populates="department")
    tickets = relationship("Ticket", back_populates="department")
