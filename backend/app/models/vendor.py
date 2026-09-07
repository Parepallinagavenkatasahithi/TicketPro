from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True, index=True)
    code = Column(String(50), nullable=False, unique=True)
    contact_name = Column(String(150), nullable=True)
    contact_email = Column(String(150), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    support_portal = Column(String(255), nullable=True)
    sla_notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=5.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    contracts = relationship("Contract", back_populates="vendor", cascade="all, delete-orphan")
    licenses = relationship("SoftwareLicense", back_populates="vendor", cascade="all, delete-orphan")


class SoftwareLicense(Base):
    __tablename__ = "software_licenses"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    software_name = Column(String(150), nullable=False)
    license_key = Column(String(255), nullable=True)
    license_type = Column(String(50), nullable=False, default="PERPETUAL") # PERPETUAL, SUBSCRIPTION, PER_USER, SITE
    total_seats = Column(Integer, default=1)
    allocated_seats = Column(Integer, default=0)
    cost_per_seat = Column(Float, default=0.0)
    purchase_date = Column(DateTime(timezone=True), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    vendor = relationship("Vendor", back_populates="licenses")
