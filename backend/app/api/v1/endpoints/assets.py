from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.asset import AssetOut, AssetCreate, AssetUpdate
from app.services.asset_service import AssetService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[AssetOut])
def list_assets(
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    assets = service.list_assets(category=category, status=status, search=search)
    results = []
    for a in assets:
        results.append(AssetOut(
            id=a.id,
            asset_tag=a.asset_tag,
            name=a.name,
            category=a.category,
            model_number=a.model_number,
            serial_number=a.serial_number,
            status=a.status,
            assigned_to_user_id=a.assigned_to_user_id,
            assigned_to_user_name=a.assigned_user.full_name if a.assigned_user else None,
            department_id=a.department_id,
            department_name=a.department.name if a.department else None,
            location=a.location,
            purchase_date=a.purchase_date,
            warranty_expiry_date=a.warranty_expiry_date,
            purchase_cost=a.purchase_cost,
            vendor_name=a.vendor_name,
            notes=a.notes,
            created_at=a.created_at,
            updated_at=a.updated_at
        ))
    return results

@router.post("", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
def create_asset(
    asset_in: AssetCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    a = service.create_asset(asset_in)
    return AssetOut.model_validate(a)
