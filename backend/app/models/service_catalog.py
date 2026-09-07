from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class ServiceCatalogCategory(Base):
    __tablename__ = "service_catalog_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    icon_name = Column(String(50), default="Package")
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    items = relationship("ServiceCatalogItem", back_populates="category", cascade="all, delete-orphan")


class ServiceCatalogItem(Base):
    __tablename__ = "service_catalog_items"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("service_catalog_categories.id"), nullable=False)
    name = Column(String(150), nullable=False)
    short_description = Column(String(255), nullable=False)
    full_description = Column(Text, nullable=True)
    estimated_fulfillment_hours = Column(Float, default=24.0)
    requires_approval = Column(Boolean, default=False)
    target_department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    cost = Column(Float, default=0.0)
    icon_name = Column(String(50), default="Wrench")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    category = relationship("ServiceCatalogCategory", back_populates="items")
    target_department = relationship("Department")
