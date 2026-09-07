from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


class PermissionOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category: str

    model_config = ConfigDict(from_attributes=True)


class RoleOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_system: bool
    permissions: List[PermissionOut] = []

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: int
    employee_id: str
    email: EmailStr
    full_name: str
    job_title: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    role_id: int
    role_name: str
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    is_active: bool
    is_verified: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    job_title: Optional[str] = None
    phone: Optional[str] = None
    role_name: str = "EMPLOYEE"
    department_id: Optional[int] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    role_name: Optional[str] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None
