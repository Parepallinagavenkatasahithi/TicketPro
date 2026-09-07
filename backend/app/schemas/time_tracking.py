from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TimeEntryOut(BaseModel):
    id: int
    ticket_id: int
    ticket_number: Optional[str] = None
    user_id: int
    user_name: Optional[str] = None
    hours_spent: float
    activity_type: str
    description: Optional[str] = None
    logged_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TimeEntryCreate(BaseModel):
    ticket_id: int
    hours_spent: float
    activity_type: str = "RESEARCH"
    description: Optional[str] = None
