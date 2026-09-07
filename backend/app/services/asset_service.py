from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate
from app.core.exceptions import NotFoundError, ValidationError

class AssetService:
    def __init__(self, db: Session):
        self.db = db

    def list_assets(self, category: Optional[str] = None, status: Optional[str] = None, search: Optional[str] = None) -> List[Asset]:
        query = self.db.query(Asset)
        if category:
            query = query.filter(Asset.category == category.upper())
        if status:
            query = query.filter(Asset.status == status.upper())
        if search:
            pattern = f"%{search}%"
            query = query.filter((Asset.asset_tag.ilike(pattern)) | (Asset.name.ilike(pattern)))
        return query.order_by(Asset.created_at.desc()).all()

    def create_asset(self, asset_in: AssetCreate) -> Asset:
        existing = self.db.query(Asset).filter(Asset.asset_tag == asset_in.asset_tag).first()
        if existing:
            raise ValidationError(f"Asset tag '{asset_in.asset_tag}' already exists")
        asset = Asset(
            asset_tag=asset_in.asset_tag,
            name=asset_in.name,
            category=asset_in.category.upper(),
            model_number=asset_in.model_number,
            serial_number=asset_in.serial_number,
            status=asset_in.status.upper(),
            assigned_to_user_id=asset_in.assigned_to_user_id,
            department_id=asset_in.department_id,
            location=asset_in.location,
            purchase_cost=asset_in.purchase_cost,
            vendor_name=asset_in.vendor_name,
            notes=asset_in.notes,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset
