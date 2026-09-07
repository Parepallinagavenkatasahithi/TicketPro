from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.change_request import ChangeRequestOut, ChangeRequestCreate
from app.services.change_management_service import ChangeManagementService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[ChangeRequestOut])
def list_change_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ChangeManagementService(db)
    chgs = service.list_change_requests()
    results = []
    for c in chgs:
        results.append(ChangeRequestOut(
            id=c.id,
            change_number=c.change_number,
            title=c.title,
            description=c.description,
            reason_for_change=c.reason_for_change,
            impact_analysis=c.impact_analysis,
            rollback_plan=c.rollback_plan,
            category=c.category,
            risk_level=c.risk_level,
            status=c.status,
            requester_id=c.requester_id,
            requester_name=c.requester.full_name if c.requester else "User",
            assigned_cab_lead_id=c.assigned_cab_lead_id,
            assigned_cab_lead_name=c.cab_lead.full_name if c.cab_lead else None,
            scheduled_start_at=c.scheduled_start_at,
            scheduled_end_at=c.scheduled_end_at,
            created_at=c.created_at,
            updated_at=c.updated_at
        ))
    return results

@router.post("", response_model=ChangeRequestOut, status_code=status.HTTP_201_CREATED)
def create_change_request(
    chg_in: ChangeRequestCreate,
    current_user: User = Depends(require_permission("ticket.create")),
    db: Session = Depends(get_db)
):
    service = ChangeManagementService(db)
    c = service.create_change_request(chg_in, current_user)
    return ChangeRequestOut.model_validate(c)
