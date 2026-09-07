from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProblemOut(BaseModel):
    id: int
    problem_number: str
    title: str
    description: str
    root_cause: Optional[str] = None
    workaround: Optional[str] = None
    status: str
    impact: str
    owner_id: int
    owner_name: Optional[str] = None
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProblemCreate(BaseModel):
    title: str
    description: str
    root_cause: Optional[str] = None
    workaround: Optional[str] = None
    impact: str = "MEDIUM"
    department_id: Optional[int] = None


class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    root_cause: Optional[str] = None
    workaround: Optional[str] = None
    status: Optional[str] = None
    impact: Optional[str] = None
    department_id: Optional[int] = None
