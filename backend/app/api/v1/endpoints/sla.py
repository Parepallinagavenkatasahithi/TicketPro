from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.sla import SLAPolicyOut, SLAPolicyCreate, SLAPolicyUpdate, SLABreachOut
from app.models.sla import SLAPolicy, SLABreach
from app.services.sla_service import SLAService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()


@router.get("/policies", response_model=List[SLAPolicyOut])
def get_sla_policies(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = SLAService(db)
    policies = service.get_policies()
    return [SLAPolicyOut.model_validate(p) for p in policies]


@router.post("/policies", response_model=SLAPolicyOut, status_code=status.HTTP_201_CREATED)
def create_sla_policy(
    policy_in: SLAPolicyCreate,
    current_user: User = Depends(require_permission("sla.manage")),
    db: Session = Depends(get_db)
):
    service = SLAService(db)
    policy = service.create_policy(policy_in)
    return SLAPolicyOut.model_validate(policy)


@router.get("/breaches", response_model=List[SLABreachOut])
def get_sla_breaches(current_user: User = Depends(require_permission("sla.manage")), db: Session = Depends(get_db)):
    breaches = db.query(SLABreach).order_by(SLABreach.breached_at.desc()).limit(100).all()
    results = []
    for b in breaches:
        results.append(SLABreachOut(
            id=b.id,
            ticket_id=b.ticket_id,
            ticket_number=b.ticket.ticket_number if b.ticket else "N/A",
            breach_type=b.breach_type,
            agent_id=b.agent_id,
            agent_name=b.agent.full_name if b.agent else None,
            expected_at=b.expected_at,
            actual_at=b.actual_at,
            breached_at=b.breached_at,
            reason=b.reason
        ))
    return results


@router.post("/evaluate", status_code=status.HTTP_200_OK)
def evaluate_sla_breaches(current_user: User = Depends(require_permission("sla.manage")), db: Session = Depends(get_db)):
    service = SLAService(db)
    breached_count = service.evaluate_all_active_tickets_sla()
    return {"message": f"SLA evaluation complete. {breached_count} new breaches logged."}
