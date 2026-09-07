from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User, Role, Permission
from app.models.department import Department
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.core.exceptions import NotFoundError, ValidationError


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_users(self, role: Optional[str] = None, department_id: Optional[int] = None, search: Optional[str] = None) -> List[User]:
        query = self.db.query(User)
        if role:
            query = query.filter(User.role_name == role.upper())
        if department_id:
            query = query.filter(User.department_id == department_id)
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (User.full_name.ilike(search_pattern)) |
                (User.email.ilike(search_pattern)) |
                (User.employee_id.ilike(search_pattern))
            )
        return query.order_by(User.id.desc()).all()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError("User", str(user_id))
        return user

    def create_user(self, user_in: UserCreate) -> User:
        existing = self.db.query(User).filter(User.email == user_in.email).first()
        if existing:
            raise ValidationError("Email already in use")

        role = self.db.query(Role).filter(Role.name == user_in.role_name.upper()).first()
        if not role:
            role = self.db.query(Role).filter(Role.name == "EMPLOYEE").first()
            role_name = "EMPLOYEE"
            role_id = role.id if role else 1
        else:
            role_name = role.name
            role_id = role.id

        count = self.db.query(User).count()
        employee_id = f"EMP-{1000 + count + 1}"

        user = User(
            employee_id=employee_id,
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            job_title=user_in.job_title,
            phone=user_in.phone,
            role_id=role_id,
            role_name=role_name,
            department_id=user_in.department_id,
            is_active=True,
            is_verified=True
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, user_in: UserUpdate) -> User:
        user = self.get_user_by_id(user_id)
        if user_in.full_name is not None:
            user.full_name = user_in.full_name
        if user_in.job_title is not None:
            user.job_title = user_in.job_title
        if user_in.phone is not None:
            user.phone = user_in.phone
        if user_in.department_id is not None:
            user.department_id = user_in.department_id
        if user_in.is_active is not None:
            user.is_active = user_in.is_active
        if user_in.role_name is not None:
            role = self.db.query(Role).filter(Role.name == user_in.role_name.upper()).first()
            if role:
                user.role_id = role.id
                user.role_name = role.name

        self.db.commit()
        self.db.refresh(user)
        return user
