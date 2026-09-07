from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[UserOut])
def get_users(
    role: Optional[str] = None,
    department_id: Optional[int] = None,
    search: Optional[str] = None,
    current_user: User = Depends(require_permission("employee.view")),
    db: Session = Depends(get_db)
):
    service = UserService(db)
    users = service.get_users(role=role, department_id=department_id, search=search)
    return [UserOut.model_validate(u) for u in users]


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    current_user: User = Depends(require_permission("employee.manage")),
    db: Session = Depends(get_db)
):
    service = UserService(db)
    user = service.create_user(user_in)
    return UserOut.model_validate(user)


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = UserService(db)
    user = service.get_user_by_id(user_id)
    return UserOut.model_validate(user)


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(require_permission("employee.manage")),
    db: Session = Depends(get_db)
):
    service = UserService(db)
    user = service.update_user(user_id, user_in)
    return UserOut.model_validate(user)
