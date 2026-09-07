from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class ApprovalStepOut(BaseModel):
    id: int
    step_number: int
    approver_id: int
    approver_name: str
    status: str
    decision_notes: Optional[str] = None
    decided_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ApprovalRequestOut(BaseModel):
    id: int
    ticket_id: int
    ticket_number: str
    requester_id: int
    requester_name: str
    title: str
    rationale: Optional[str] = None
    status: str
    created_at: datetime
    steps: List[ApprovalStepOut] = []

    model_config = ConfigDict(from_attributes=True)


class ApprovalRequestCreate(BaseModel):
    ticket_id: int
    title: str
    rationale: Optional[str] = None
    approver_ids: List[int]


class ApprovalDecisionRequest(BaseModel):
    decision: str  # APPROVED or REJECTED
    notes: Optional[str] = None
