from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.on_call import OnCallRotationOut, OnCallRotationCreate, OnCallShiftOut, OnCallShiftCreate
from app.services.on_call_service import OnCallService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[OnCallRotationOut])
def list_rotations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = OnCallService(db)
    rots = service.list_rotations()
    results = []
    for r in rots:
        shifts_out = []
        for s in r.shifts:
            shifts_out.append(OnCallShiftOut(
                id=s.id,
                rotation_id=s.rotation_id,
                user_id=s.user_id,
                primary_user_name=s.primary_user.full_name if s.primary_user else None,
                start_at=s.start_at,
                end_at=s.end_at,
                override_user_id=s.override_user_id,
                override_user_name=s.override_user.full_name if s.override_user else None,
                notes=s.notes,
                created_at=s.created_at
            ))
        results.append(OnCallRotationOut(
            id=r.id,
            name=r.name,
            department_id=r.department_id,
            department_name=r.department.name if r.department else None,
            rotation_type=r.rotation_type,
            start_time=r.start_time,
            time_zone=r.time_zone,
            is_active=r.is_active,
            created_at=r.created_at,
            shifts=shifts_out
        ))
    return results

@router.post("", response_model=OnCallRotationOut, status_code=status.HTTP_201_CREATED)
def create_rotation(
    rot_in: OnCallRotationCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    service = OnCallService(db)
    r = service.create_rotation(rot_in)
    return OnCallRotationOut.model_validate(r)

@router.post("/shifts", response_model=OnCallShiftOut, status_code=status.HTTP_201_CREATED)
def create_shift(
    shift_in: OnCallShiftCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    service = OnCallService(db)
    s = service.create_shift(shift_in)
    return OnCallShiftOut.model_validate(s)
