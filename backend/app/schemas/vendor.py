from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr


class VendorBase(BaseModel):
    name: str
    code: str
    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    support_portal: Optional[str] = None
    sla_notes: Optional[str] = None
    is_active: bool = True
    rating: float = 5.0


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    support_portal: Optional[str] = None
    sla_notes: Optional[str] = None
    is_active: Optional[bool] = None
    rating: Optional[float] = None


class VendorOut(VendorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SoftwareLicenseBase(BaseModel):
    vendor_id: int
    software_name: str
    license_key: Optional[str] = None
    license_type: str = "PERPETUAL"
    total_seats: int = 1
    allocated_seats: int = 0
    cost_per_seat: float = 0.0
    purchase_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    is_active: bool = True


class SoftwareLicenseCreate(SoftwareLicenseBase):
    pass


class SoftwareLicenseOut(SoftwareLicenseBase):
    id: int
    vendor_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
