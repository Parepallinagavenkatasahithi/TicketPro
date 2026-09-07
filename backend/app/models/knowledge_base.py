from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class KnowledgeBaseArticle(Base):
    __tablename__ = "knowledge_base_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("ticket_categories.id", ondelete="SET NULL"), nullable=True)
    
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(30), default="PUBLISHED", index=True)  # DRAFT, PUBLISHED, ARCHIVED
    
    view_count = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    unhelpful_count = Column(Integer, default=0)
    tags = Column(String(255), nullable=True)  # comma separated
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    category = relationship("TicketCategory")
    author = relationship("User")
