from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.knowledge_base import ArticleOut, ArticleCreate, ArticleUpdate, ArticleFeedback
from app.services.kb_service import KBService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[ArticleOut])
def list_articles(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    status: str = "PUBLISHED",
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = KBService(db)
    articles, total = service.list_articles(category_id=category_id, search=search, status=status, skip=skip, limit=limit)
    results = []
    for a in articles:
        results.append(ArticleOut(
            id=a.id,
            title=a.title,
            slug=a.slug,
            category_id=a.category_id,
            category_name=a.category.name if a.category else None,
            content=a.content,
            author_id=a.author_id,
            author_name=a.author.full_name if a.author else "Support Team",
            status=a.status,
            view_count=a.view_count,
            helpful_count=a.helpful_count,
            unhelpful_count=a.unhelpful_count,
            tags=a.tags,
            created_at=a.created_at,
            updated_at=a.updated_at
        ))
    return results


@router.post("", response_model=ArticleOut, status_code=status.HTTP_201_CREATED)
def create_article(
    article_in: ArticleCreate,
    current_user: User = Depends(require_permission("kb.manage")),
    db: Session = Depends(get_db)
):
    service = KBService(db)
    a = service.create_article(article_in, current_user)
    return ArticleOut(
        id=a.id,
        title=a.title,
        slug=a.slug,
        category_id=a.category_id,
        category_name=a.category.name if a.category else None,
        content=a.content,
        author_id=a.author_id,
        author_name=current_user.full_name,
        status=a.status,
        view_count=a.view_count,
        helpful_count=a.helpful_count,
        unhelpful_count=a.unhelpful_count,
        tags=a.tags,
        created_at=a.created_at,
        updated_at=a.updated_at
    )


@router.get("/{identifier}", response_model=ArticleOut)
def get_article(
    identifier: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = KBService(db)
    a = service.get_article_by_id_or_slug(identifier)
    return ArticleOut(
        id=a.id,
        title=a.title,
        slug=a.slug,
        category_id=a.category_id,
        category_name=a.category.name if a.category else None,
        content=a.content,
        author_id=a.author_id,
        author_name=a.author.full_name if a.author else "Support Team",
        status=a.status,
        view_count=a.view_count,
        helpful_count=a.helpful_count,
        unhelpful_count=a.unhelpful_count,
        tags=a.tags,
        created_at=a.created_at,
        updated_at=a.updated_at
    )


@router.post("/{article_id}/feedback", response_model=ArticleOut)
def rate_article(
    article_id: int,
    feedback: ArticleFeedback,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = KBService(db)
    a = service.rate_helpfulness(article_id, feedback.is_helpful)
    return ArticleOut(
        id=a.id,
        title=a.title,
        slug=a.slug,
        category_id=a.category_id,
        category_name=a.category.name if a.category else None,
        content=a.content,
        author_id=a.author_id,
        author_name=a.author.full_name if a.author else "Support Team",
        status=a.status,
        view_count=a.view_count,
        helpful_count=a.helpful_count,
        unhelpful_count=a.unhelpful_count,
        tags=a.tags,
        created_at=a.created_at,
        updated_at=a.updated_at
    )
