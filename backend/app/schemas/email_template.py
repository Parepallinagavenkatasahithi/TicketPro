from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class EmailTemplateBase(BaseModel):
    name: str
    event_trigger: str
    subject_template: str
    body_template: str
    is_active: bool = True
    description: Optional[str] = None


class EmailTemplateCreate(EmailTemplateBase):
    pass


class EmailTemplateOut(EmailTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
