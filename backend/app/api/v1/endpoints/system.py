from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.system import SystemSettingOut, SystemSettingUpdate, IntegrationOut, IntegrationUpdate
from app.models.system import SystemSetting, Integration
from app.security.rbac import require_permission
from app.models.user import User

router = APIRouter()


@router.get("/settings", response_model=List[SystemSettingOut])
def get_system_settings(current_user: User = Depends(require_permission("settings.manage")), db: Session = Depends(get_db)):
    settings = db.query(SystemSetting).all()
    return [SystemSettingOut.model_validate(s) for s in settings]


@router.get("/integrations", response_model=List[IntegrationOut])
def get_integrations(current_user: User = Depends(require_permission("settings.manage")), db: Session = Depends(get_db)):
    integrations = db.query(Integration).all()
    return [IntegrationOut.model_validate(i) for i in integrations]


@router.put("/integrations/{integration_id}", response_model=IntegrationOut)
def update_integration(
    integration_id: int,
    integ_in: IntegrationUpdate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    integ = db.query(Integration).filter(Integration.id == integration_id).first()
    if integ:
        integ.is_active = integ_in.is_active
        if integ_in.config_json:
            integ.config_json = integ_in.config_json
        db.commit()
        db.refresh(integ)
    return IntegrationOut.model_validate(integ)
