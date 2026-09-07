from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class SLAPolicyOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    priority: str
    max_first_response_minutes: int
    max_resolution_minutes: int
    warning_threshold_percent: float
    is_default: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SLAPolicyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    priority: str
    max_first_response_minutes: int
    max_resolution_minutes: int
    warning_threshold_percent: float = 80.0
    is_default: bool = False


class SLAPolicyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    max_first_response_minutes: Optional[int] = None
    max_resolution_minutes: Optional[int] = None
    warning_threshold_percent: Optional[float] = None
    is_active: Optional[bool] = None


class SLABreachOut(BaseModel):
    id: int
    ticket_id: int
    ticket_number: str
    breach_type: str
    agent_id: Optional[int] = None
    agent_name: Optional[str] = None
    expected_at: datetime
    actual_at: Optional[datetime] = None
    breached_at: datetime
    reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
