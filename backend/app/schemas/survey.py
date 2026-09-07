from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SurveyOut(BaseModel):
    id: int
    ticket_id: int
    ticket_number: Optional[str] = None
    respondent_id: int
    respondent_name: Optional[str] = None
    rating: int
    feedback_text: Optional[str] = None
    agent_id: Optional[int] = None
    agent_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SurveyCreate(BaseModel):
    ticket_id: int
    rating: int
    feedback_text: Optional[str] = None
