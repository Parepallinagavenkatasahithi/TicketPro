from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class AnnouncementOut(BaseModel):
    id: int
    title: str
    content: str
    priority: str
    target_audience: str
    status: str
    author_id: int
    author_name: str
    published_at: Optional[datetime] = None
    scheduled_for: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnnouncementCreate(BaseModel):
    title: str
    content: str
    priority: str = "NORMAL"
    target_audience: str = "ALL"
    status: str = "PUBLISHED"
    scheduled_for: Optional[datetime] = None


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[str] = None
    target_audience: Optional[str] = None
    status: Optional[str] = None
    scheduled_for: Optional[datetime] = None
