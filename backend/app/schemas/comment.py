from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    content: str
    is_internal_note: bool = False


class CommentOut(BaseModel):
    id: int
    ticket_id: int
    author_id: int
    author_name: str
    author_role: str
    author_avatar: Optional[str] = None
    content: str
    is_internal_note: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
