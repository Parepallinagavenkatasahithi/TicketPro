from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.service_catalog import ServiceCatalogCategoryOut, ServiceCatalogCategoryCreate, ServiceCatalogItemOut, ServiceCatalogItemCreate
from app.services.service_catalog_service import ServiceCatalogService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("/categories", response_model=List[ServiceCatalogCategoryOut])
def list_categories(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ServiceCatalogService(db)
    cats = service.list_categories()
    return [ServiceCatalogCategoryOut.model_validate(c) for c in cats]

@router.post("/categories", response_model=ServiceCatalogCategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    cat_in: ServiceCatalogCategoryCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    service = ServiceCatalogService(db)
    cat = service.create_category(cat_in)
    return ServiceCatalogCategoryOut.model_validate(cat)

@router.get("/items", response_model=List[ServiceCatalogItemOut])
def list_items(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ServiceCatalogService(db)
    items = service.list_items()
    results = []
    for i in items:
        results.append(ServiceCatalogItemOut(
            id=i.id,
            category_id=i.category_id,
            category_name=i.category.name if i.category else None,
            name=i.name,
            short_description=i.short_description,
            full_description=i.full_description,
            estimated_fulfillment_hours=i.estimated_fulfillment_hours,
            requires_approval=i.requires_approval,
            target_department_id=i.target_department_id,
            target_department_name=i.target_department.name if i.target_department else None,
            is_active=i.is_active,
            cost=i.cost,
            icon_name=i.icon_name,
            created_at=i.created_at
        ))
    return results

@router.post("/items", response_model=ServiceCatalogItemOut, status_code=status.HTTP_201_CREATED)
def create_item(
    item_in: ServiceCatalogItemCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    service = ServiceCatalogService(db)
    i = service.create_item(item_in)
    return ServiceCatalogItemOut.model_validate(i)
