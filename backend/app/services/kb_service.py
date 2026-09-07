import re
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.knowledge_base import KnowledgeBaseArticle
from app.models.user import User
from app.schemas.knowledge_base import ArticleCreate, ArticleUpdate
from app.core.exceptions import NotFoundError, ValidationError


class KBService:
    def __init__(self, db: Session):
        self.db = db

    def generate_slug(self, title: str) -> str:
        slug = title.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_-]+', '-', slug)
        
        # Check uniqueness
        count = self.db.query(KnowledgeBaseArticle).filter(KnowledgeBaseArticle.slug.like(f"{slug}%")).count()
        if count > 0:
            slug = f"{slug}-{count + 1}"
        return slug

    def list_articles(
        self,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
        status: str = "PUBLISHED",
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[KnowledgeBaseArticle], int]:
        query = self.db.query(KnowledgeBaseArticle)
        if status:
            query = query.filter(KnowledgeBaseArticle.status == status.upper())
        if category_id:
            query = query.filter(KnowledgeBaseArticle.category_id == category_id)
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    KnowledgeBaseArticle.title.ilike(pattern),
                    KnowledgeBaseArticle.content.ilike(pattern),
                    KnowledgeBaseArticle.tags.ilike(pattern)
                )
            )

        total = query.count()
        articles = query.order_by(KnowledgeBaseArticle.created_at.desc()).offset(skip).limit(limit).all()
        return articles, total

    def get_article_by_id_or_slug(self, identifier: str) -> KnowledgeBaseArticle:
        if identifier.isdigit():
            article = self.db.query(KnowledgeBaseArticle).filter(KnowledgeBaseArticle.id == int(identifier)).first()
        else:
            article = self.db.query(KnowledgeBaseArticle).filter(KnowledgeBaseArticle.slug == identifier).first()

        if not article:
            raise NotFoundError("Knowledge Base Article", identifier)

        # Increment view count
        article.view_count += 1
        self.db.commit()
        return article

    def create_article(self, article_in: ArticleCreate, author: User) -> KnowledgeBaseArticle:
        slug = self.generate_slug(article_in.title)
        article = KnowledgeBaseArticle(
            title=article_in.title,
            slug=slug,
            category_id=article_in.category_id,
            content=article_in.content,
            author_id=author.id,
            status=article_in.status.upper(),
            tags=article_in.tags,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

    def rate_helpfulness(self, article_id: int, is_helpful: bool) -> KnowledgeBaseArticle:
        article = self.get_article_by_id_or_slug(str(article_id))
        if is_helpful:
            article.helpful_count += 1
        else:
            article.unhelpful_count += 1
        self.db.commit()
        self.db.refresh(article)
        return article
