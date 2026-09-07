from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class ServiceCatalogCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon_name: str = "Package"
    display_order: int = 0
    is_active: bool = True


class ServiceCatalogCategoryCreate(ServiceCatalogCategoryBase):
    pass


class ServiceCatalogCategoryOut(ServiceCatalogCategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ServiceCatalogItemBase(BaseModel):
    category_id: int
    name: str
    short_description: str
    full_description: Optional[str] = None
    estimated_fulfillment_hours: float = 24.0
    requires_approval: bool = False
    target_department_id: Optional[int] = None
    is_active: bool = True
    cost: float = 0.0
    icon_name: str = "Wrench"


class ServiceCatalogItemCreate(ServiceCatalogItemBase):
    pass


class ServiceCatalogItemOut(ServiceCatalogItemBase):
    id: int
    category_name: Optional[str] = None
    target_department_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
