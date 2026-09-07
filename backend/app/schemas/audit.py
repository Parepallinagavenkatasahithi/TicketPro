from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class AuditLogOut(BaseModel):
    id: int
    actor_id: Optional[int] = None
    actor_name: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    changes_json: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
