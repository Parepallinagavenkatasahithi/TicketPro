from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class DepartmentOut(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None
    manager_id: Optional[int] = None
    manager_name: Optional[str] = None
    member_count: int = 0
    open_ticket_count: int = 0
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DepartmentCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    manager_id: Optional[int] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None
