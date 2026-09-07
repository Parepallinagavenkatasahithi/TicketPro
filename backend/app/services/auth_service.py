from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.models.user import User, Role
from app.schemas.auth import LoginRequest, UserRegister
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.core.exceptions import AuthenticationError, ValidationError


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, login_data: LoginRequest) -> User:
        user = self.db.query(User).filter(User.email == login_data.email).first()
        if not user:
            raise AuthenticationError("Invalid email or password")
        if not verify_password(login_data.password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")
        if not user.is_active:
            raise AuthenticationError("User account is deactivated")
        return user

    def register_user(self, register_data: UserRegister) -> User:
        existing = self.db.query(User).filter(User.email == register_data.email).first()
        if existing:
            raise ValidationError("An account with this email already exists")

        # Generate Employee ID (EMP-100X)
        count = self.db.query(User).count()
        employee_id = f"EMP-{1000 + count + 1}"

        role = self.db.query(Role).filter(Role.name == "EMPLOYEE").first()
        role_id = role.id if role else 1

        hashed_pwd = get_password_hash(register_data.password)
        new_user = User(
            employee_id=employee_id,
            email=register_data.email,
            hashed_password=hashed_pwd,
            full_name=register_data.full_name,
            job_title=register_data.job_title,
            phone=register_data.phone,
            role_id=role_id,
            role_name="EMPLOYEE",
            department_id=register_data.department_id,
            is_active=True,
            is_verified=True
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def create_tokens_for_user(self, user: User) -> Tuple[str, str]:
        extra_claims = {
            "role": user.role_name,
            "email": user.email,
            "name": user.full_name
        }
        access_token = create_access_token(user.id, extra_claims=extra_claims)
        refresh_token = create_refresh_token(user.id)
        return access_token, refresh_token
