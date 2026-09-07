from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, UserRegister
from app.schemas.user import UserOut
from app.services.auth_service import AuthService
from app.services.audit_service import AuditService
from app.security.rbac import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(login_data)
    access_token, refresh_token = auth_service.create_tokens_for_user(user)
    
    # Audit log
    audit_service = AuditService(db)
    audit_service.log_event(
        action="USER_LOGIN",
        resource_type="USER",
        actor_id=user.id,
        resource_id=str(user.id),
        ip_address=request.client.host if request.client else None
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=86400,
        refresh_token=refresh_token,
        user=UserOut.model_validate(user)
    )


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(register_data: UserRegister, request: Request, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.register_user(register_data)

    audit_service = AuditService(db)
    audit_service.log_event(
        action="USER_REGISTER",
        resource_type="USER",
        actor_id=user.id,
        resource_id=str(user.id),
        ip_address=request.client.host if request.client else None
    )

    return UserOut.model_validate(user)


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    audit_service = AuditService(db)
    audit_service.log_event(
        action="USER_LOGOUT",
        resource_type="USER",
        actor_id=current_user.id,
        resource_id=str(current_user.id)
    )
    return {"message": "Successfully logged out"}
