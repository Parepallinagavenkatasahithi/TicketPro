from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.announcement import AnnouncementOut, AnnouncementCreate, AnnouncementUpdate
from app.services.announcement_service import AnnouncementService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[AnnouncementOut])
def get_announcements(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AnnouncementService(db)
    announcements = service.list_announcements(current_user=current_user, status=status)
    results = []
    for a in announcements:
        results.append(AnnouncementOut(
            id=a.id,
            title=a.title,
            content=a.content,
            priority=a.priority,
            target_audience=a.target_audience,
            status=a.status,
            author_id=a.author_id,
            author_name=a.author.full_name if a.author else "Admin",
            published_at=a.published_at,
            scheduled_for=a.scheduled_for,
            created_at=a.created_at
        ))
    return results


@router.post("", response_model=AnnouncementOut, status_code=status.HTTP_201_CREATED)
def create_announcement(
    announcement_in: AnnouncementCreate,
    current_user: User = Depends(require_permission("announcements.create")),
    db: Session = Depends(get_db)
):
    service = AnnouncementService(db)
    a = service.create_announcement(announcement_in, current_user)
    return AnnouncementOut(
        id=a.id,
        title=a.title,
        content=a.content,
        priority=a.priority,
        target_audience=a.target_audience,
        status=a.status,
        author_id=a.author_id,
        author_name=current_user.full_name,
        published_at=a.published_at,
        scheduled_for=a.scheduled_for,
        created_at=a.created_at
    )
