from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.vendor import Vendor, SoftwareLicense
from app.schemas.vendor import VendorCreate, VendorUpdate, SoftwareLicenseCreate


class VendorService:
    def __init__(self, db: Session):
        self.db = db

    def list_vendors(self) -> List[Vendor]:
        return self.db.query(Vendor).order_by(Vendor.name.asc()).all()

    def create_vendor(self, vendor_in: VendorCreate) -> Vendor:
        v = Vendor(**vendor_in.model_dump())
        self.db.add(v)
        self.db.commit()
        self.db.refresh(v)
        return v

    def list_licenses(self) -> List[SoftwareLicense]:
        return self.db.query(SoftwareLicense).order_by(SoftwareLicense.software_name.asc()).all()

    def create_license(self, lic_in: SoftwareLicenseCreate) -> SoftwareLicense:
        lic = SoftwareLicense(**lic_in.model_dump())
        self.db.add(lic)
        self.db.commit()
        self.db.refresh(lic)
        return lic
