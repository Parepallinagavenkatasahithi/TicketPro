from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.problem import ProblemOut, ProblemCreate
from app.services.problem_management_service import ProblemManagementService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[ProblemOut])
def list_problems(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ProblemManagementService(db)
    prbs = service.list_problems()
    results = []
    for p in prbs:
        results.append(ProblemOut(
            id=p.id,
            problem_number=p.problem_number,
            title=p.title,
            description=p.description,
            root_cause=p.root_cause,
            workaround=p.workaround,
            status=p.status,
            impact=p.impact,
            owner_id=p.owner_id,
            owner_name=p.owner.full_name if p.owner else "Owner",
            department_id=p.department_id,
            department_name=p.department.name if p.department else None,
            resolved_at=p.resolved_at,
            created_at=p.created_at
        ))
    return results

@router.post("", response_model=ProblemOut, status_code=status.HTTP_201_CREATED)
def create_problem(
    prb_in: ProblemCreate,
    current_user: User = Depends(require_permission("ticket.create")),
    db: Session = Depends(get_db)
):
    service = ProblemManagementService(db)
    p = service.create_problem(prb_in, current_user)
    return ProblemOut.model_validate(p)
