from typing import List, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.core.exceptions import AuthenticationError, PermissionDeniedError
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

ROLE_PERMISSIONS = {
    "ADMIN": [
        "ticket.create", "ticket.view", "ticket.edit", "ticket.assign", "ticket.resolve",
        "ticket.close", "ticket.reopen", "ticket.delete", "ticket.comment", "ticket.internal_note",
        "employee.view", "employee.manage", "department.manage", "sla.manage", "approvals.manage",
        "announcements.manage", "kb.manage", "reports.view", "audit.view", "settings.manage"
    ],
    "MANAGER": [
        "ticket.create", "ticket.view", "ticket.edit", "ticket.assign", "ticket.resolve",
        "ticket.close", "ticket.reopen", "ticket.comment", "ticket.internal_note",
        "employee.view", "department.view", "sla.view", "approvals.manage",
        "announcements.create", "kb.manage", "reports.view"
    ],
    "AGENT": [
        "ticket.create", "ticket.view", "ticket.edit", "ticket.assign", "ticket.resolve",
        "ticket.close", "ticket.reopen", "ticket.comment", "ticket.internal_note",
        "employee.view", "kb.manage"
    ],
    "EMPLOYEE": [
        "ticket.create", "ticket.view", "ticket.reopen", "ticket.comment", "kb.view"
    ]
}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise AuthenticationError("Invalid or expired authentication token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationError("Token payload missing user identifier")
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise AuthenticationError("User account no longer exists")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is deactivated")
        
    return user


def require_permission(required_permission: str):
    def permission_checker(current_user: User = Depends(get_current_user)):
        user_role = current_user.role_name
        permissions = ROLE_PERMISSIONS.get(user_role, [])
        if required_permission not in permissions and user_role != "ADMIN":
            raise PermissionDeniedError(f"Action requires '{required_permission}' permission")
        return current_user
    return permission_checker


def require_roles(allowed_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role_name not in allowed_roles and current_user.role_name != "ADMIN":
            raise PermissionDeniedError(f"Role must be one of {allowed_roles}")
        return current_user
    return role_checker
