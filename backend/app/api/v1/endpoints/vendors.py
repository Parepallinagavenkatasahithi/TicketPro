from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.vendor import VendorOut, VendorCreate, SoftwareLicenseOut, SoftwareLicenseCreate
from app.services.vendor_service import VendorService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[VendorOut])
def list_vendors(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = VendorService(db)
    vendors = service.list_vendors()
    return [VendorOut.model_validate(v) for v in vendors]

@router.post("", response_model=VendorOut, status_code=status.HTTP_201_CREATED)
def create_vendor(
    vendor_in: VendorCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    service = VendorService(db)
    v = service.create_vendor(vendor_in)
    return VendorOut.model_validate(v)

@router.get("/licenses", response_model=List[SoftwareLicenseOut])
def list_licenses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = VendorService(db)
    lics = service.list_licenses()
    results = []
    for l in lics:
        results.append(SoftwareLicenseOut(
            id=l.id,
            vendor_id=l.vendor_id,
            vendor_name=l.vendor.name if l.vendor else None,
            software_name=l.software_name,
            license_key=l.license_key,
            license_type=l.license_type,
            total_seats=l.total_seats,
            allocated_seats=l.allocated_seats,
            cost_per_seat=l.cost_per_seat,
            purchase_date=l.purchase_date,
            expiry_date=l.expiry_date,
            is_active=l.is_active,
            created_at=l.created_at,
            updated_at=l.updated_at
        ))
    return results

@router.post("/licenses", response_model=SoftwareLicenseOut, status_code=status.HTTP_201_CREATED)
def create_license(
    lic_in: SoftwareLicenseCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    service = VendorService(db)
    lic = service.create_license(lic_in)
    return SoftwareLicenseOut.model_validate(lic)
