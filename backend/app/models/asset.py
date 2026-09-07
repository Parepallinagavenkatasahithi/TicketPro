from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False) # LAPTOP, DESKTOP, SERVER, MONITOR, PRINTER, NETWORK, OTHER
    model_number = Column(String(100), nullable=True)
    serial_number = Column(String(100), unique=True, nullable=True)
    status = Column(String(30), default="IN_USE") # IN_USE, IN_STOCK, UNDER_REPAIR, RETIRED, LOST
    
    assigned_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    location = Column(String(100), nullable=True)
    
    purchase_date = Column(DateTime(timezone=True), nullable=True)
    warranty_expiry_date = Column(DateTime(timezone=True), nullable=True)
    purchase_cost = Column(Float, nullable=True)
    vendor_name = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    assigned_user = relationship("User", foreign_keys=[assigned_to_user_id])
    department = relationship("Department", foreign_keys=[department_id])
