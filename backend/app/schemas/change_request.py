from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ChangeRequestOut(BaseModel):
    id: int
    change_number: str
    title: str
    description: str
    reason_for_change: str
    impact_analysis: str
    rollback_plan: str
    category: str
    risk_level: str
    status: str
    requester_id: int
    requester_name: Optional[str] = None
    assigned_cab_lead_id: Optional[int] = None
    assigned_cab_lead_name: Optional[str] = None
    scheduled_start_at: Optional[datetime] = None
    scheduled_end_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChangeRequestCreate(BaseModel):
    title: str
    description: str
    reason_for_change: str
    impact_analysis: str
    rollback_plan: str
    category: str = "STANDARD"
    risk_level: str = "MEDIUM"
    assigned_cab_lead_id: Optional[int] = None

class ChangeRequestStatusUpdate(BaseModel):
    status: str
    decision_notes: Optional[str] = None
