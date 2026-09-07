from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class OnCallRotation(Base):
    __tablename__ = "on_call_rotations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    rotation_type = Column(String(50), default="WEEKLY") # DAILY, WEEKLY, BIWEEKLY, CUSTOM
    start_time = Column(String(20), default="09:00") # Time of day shift starts e.g. "09:00"
    time_zone = Column(String(50), default="UTC")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    department = relationship("Department")
    shifts = relationship("OnCallShift", back_populates="rotation", cascade="all, delete-orphan")


class OnCallShift(Base):
    __tablename__ = "on_call_shifts"

    id = Column(Integer, primary_key=True, index=True)
    rotation_id = Column(Integer, ForeignKey("on_call_rotations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_at = Column(DateTime(timezone=True), nullable=False)
    end_at = Column(DateTime(timezone=True), nullable=False)
    override_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    rotation = relationship("OnCallRotation", back_populates="shifts")
    primary_user = relationship("User", foreign_keys=[user_id])
    override_user = relationship("User", foreign_keys=[override_user_id])
