from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class ArticleOut(BaseModel):
    id: int
    title: str
    slug: str
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    content: str
    author_id: int
    author_name: str
    status: str
    view_count: int
    helpful_count: int
    unhelpful_count: int
    tags: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ArticleCreate(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None
    status: str = "PUBLISHED"
    tags: Optional[str] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None
    tags: Optional[str] = None


class ArticleFeedback(BaseModel):
    is_helpful: bool
