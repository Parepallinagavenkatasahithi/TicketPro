from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AssetOut(BaseModel):
    id: int
    asset_tag: str
    name: str
    category: str
    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    status: str
    assigned_to_user_id: Optional[int] = None
    assigned_to_user_name: Optional[str] = None
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    location: Optional[str] = None
    purchase_date: Optional[datetime] = None
    warranty_expiry_date: Optional[datetime] = None
    purchase_cost: Optional[float] = None
    vendor_name: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AssetCreate(BaseModel):
    asset_tag: str
    name: str
    category: str
    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    status: str = "IN_USE"
    assigned_to_user_id: Optional[int] = None
    department_id: Optional[int] = None
    location: Optional[str] = None
    purchase_cost: Optional[float] = None
    vendor_name: Optional[str] = None
    notes: Optional[str] = None

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    assigned_to_user_id: Optional[int] = None
    department_id: Optional[int] = None
    location: Optional[str] = None
    notes: Optional[str] = None
