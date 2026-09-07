from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class AttachmentOut(BaseModel):
    id: int
    ticket_id: int
    comment_id: Optional[int] = None
    uploader_id: int
    uploader_name: str
    file_name: str
    storage_path: str
    file_size: int
    mime_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
