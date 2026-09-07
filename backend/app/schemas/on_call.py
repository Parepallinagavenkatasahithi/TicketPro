from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class OnCallShiftBase(BaseModel):
    rotation_id: int
    user_id: int
    start_at: datetime
    end_at: datetime
    override_user_id: Optional[int] = None
    notes: Optional[str] = None


class OnCallShiftCreate(OnCallShiftBase):
    pass


class OnCallShiftOut(OnCallShiftBase):
    id: int
    primary_user_name: Optional[str] = None
    override_user_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OnCallRotationBase(BaseModel):
    name: str
    department_id: int
    rotation_type: str = "WEEKLY"
    start_time: str = "09:00"
    time_zone: str = "UTC"
    is_active: bool = True


class OnCallRotationCreate(OnCallRotationBase):
    pass


class OnCallRotationOut(OnCallRotationBase):
    id: int
    department_name: Optional[str] = None
    created_at: datetime
    shifts: List[OnCallShiftOut] = []

    model_config = ConfigDict(from_attributes=True)
