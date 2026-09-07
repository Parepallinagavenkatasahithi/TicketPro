from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class CustomField(Base):
    __tablename__ = "custom_fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    field_key = Column(String(100), nullable=False, unique=True)
    field_type = Column(String(50), nullable=False, default="TEXT") # TEXT, NUMBER, SELECT, CHECKBOX, DATE
    description = Column(String(255), nullable=True)
    is_required = Column(Boolean, default=False)
    options_json = Column(Text, nullable=True) # JSON list for SELECT type
    target_entity = Column(String(50), default="TICKET") # TICKET, ASSET, CHANGE
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CustomFieldValue(Base):
    __tablename__ = "custom_field_values"

    id = Column(Integer, primary_key=True, index=True)
    custom_field_id = Column(Integer, ForeignKey("custom_fields.id"), nullable=False)
    entity_id = Column(Integer, nullable=False) # e.g. ticket_id or asset_id
    field_value = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    custom_field = relationship("CustomField")
