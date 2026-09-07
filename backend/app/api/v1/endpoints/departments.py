from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.department import DepartmentOut, DepartmentCreate, DepartmentUpdate
from app.models.department import Department
from app.models.user import User
from app.models.ticket import Ticket, TicketStatus
from app.security.rbac import get_current_user, require_permission
from app.core.exceptions import NotFoundError

router = APIRouter()


@router.get("", response_model=List[DepartmentOut])
def get_departments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    depts = db.query(Department).all()
    results = []
    for d in depts:
        member_cnt = len(d.members) if d.members else 0
        open_cnt = db.query(Ticket).filter(
            Ticket.department_id == d.id,
            Ticket.status.in_([TicketStatus.OPEN.value, TicketStatus.ASSIGNED.value, TicketStatus.IN_PROGRESS.value])
        ).count()
        
        results.append(DepartmentOut(
            id=d.id,
            name=d.name,
            code=d.code,
            description=d.description,
            manager_id=d.manager_id,
            manager_name=d.manager.full_name if d.manager else None,
            member_count=member_cnt,
            open_ticket_count=open_cnt,
            created_at=d.created_at
        ))
    return results


@router.post("", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(
    dept_in: DepartmentCreate,
    current_user: User = Depends(require_permission("department.manage")),
    db: Session = Depends(get_db)
):
    dept = Department(
        name=dept_in.name,
        code=dept_in.code.upper(),
        description=dept_in.description,
        manager_id=dept_in.manager_id
    )
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return DepartmentOut(
        id=dept.id,
        name=dept.name,
        code=dept.code,
        description=dept.description,
        manager_id=dept.manager_id,
        manager_name=dept.manager.full_name if dept.manager else None,
        member_count=0,
        open_ticket_count=0,
        created_at=dept.created_at
    )
