from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.custom_field import CustomFieldOut, CustomFieldCreate, CustomFieldValueOut, CustomFieldValueCreate
from app.services.custom_field_service import CustomFieldService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[CustomFieldOut])
def list_custom_fields(target_entity: Optional[str] = "TICKET", current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = CustomFieldService(db)
    fields = service.list_custom_fields(target_entity=target_entity)
    return [CustomFieldOut.model_validate(f) for f in fields]

@router.post("", response_model=CustomFieldOut, status_code=status.HTTP_201_CREATED)
def create_custom_field(
    cf_in: CustomFieldCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    service = CustomFieldService(db)
    f = service.create_custom_field(cf_in)
    return CustomFieldOut.model_validate(f)

@router.post("/values", response_model=CustomFieldValueOut, status_code=status.HTTP_201_CREATED)
def set_custom_field_value(
    val_in: CustomFieldValueCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = CustomFieldService(db)
    v = service.set_field_value(val_in)
    return CustomFieldValueOut.model_validate(v)
