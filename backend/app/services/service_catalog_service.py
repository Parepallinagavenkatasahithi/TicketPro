from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from app.models.service_catalog import ServiceCatalogCategory, ServiceCatalogItem
from app.schemas.service_catalog import ServiceCatalogCategoryCreate, ServiceCatalogItemCreate


class ServiceCatalogService:
    def __init__(self, db: Session):
        self.db = db

    def list_categories(self) -> List[ServiceCatalogCategory]:
        return self.db.query(ServiceCatalogCategory).filter(ServiceCatalogCategory.is_active == True).order_by(ServiceCatalogCategory.display_order.asc()).all()

    def create_category(self, cat_in: ServiceCatalogCategoryCreate) -> ServiceCatalogCategory:
        cat = ServiceCatalogCategory(**cat_in.model_dump())
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def list_items(self) -> List[ServiceCatalogItem]:
        return self.db.query(ServiceCatalogItem).filter(ServiceCatalogItem.is_active == True).all()

    def create_item(self, item_in: ServiceCatalogItemCreate) -> ServiceCatalogItem:
        item = ServiceCatalogItem(**item_in.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
