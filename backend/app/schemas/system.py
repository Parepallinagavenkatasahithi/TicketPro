from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class SystemSettingOut(BaseModel):
    id: int
    key: str
    value: Optional[str] = None
    description: Optional[str] = None
    category: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SystemSettingUpdate(BaseModel):
    value: str


class IntegrationOut(BaseModel):
    id: int
    name: str
    type: str
    config_json: Optional[str] = None
    is_active: bool
    last_synced_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class IntegrationUpdate(BaseModel):
    is_active: bool
    config_json: Optional[str] = None
