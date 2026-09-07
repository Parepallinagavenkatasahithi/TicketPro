from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String(50), nullable=False, unique=True, index=True)
    title = Column(String(200), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    contract_type = Column(String(50), nullable=False, default="SLA_SUPPORT") # SLA_SUPPORT, LEASE, MAINTENANCE, CLOUD_SERVICE
    status = Column(String(50), nullable=False, default="ACTIVE") # DRAFT, ACTIVE, EXPIRED, RENEWAL_PENDING, TERMINATED
    annual_cost = Column(Float, default=0.0)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    auto_renew = Column(Boolean, default=False)
    notice_period_days = Column(Integer, default=30)
    document_url = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    vendor = relationship("Vendor", back_populates="contracts")
