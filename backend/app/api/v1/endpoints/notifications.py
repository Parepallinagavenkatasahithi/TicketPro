from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.notification import NotificationOut
from app.services.notification_service import NotificationService
from app.security.rbac import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[NotificationOut])
def get_notifications(
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    notifs = service.get_user_notifications(current_user.id, unread_only=unread_only)
    return [NotificationOut.model_validate(n) for n in notifs]


@router.put("/{notification_id}/read", response_model=NotificationOut)
def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    notif = service.mark_as_read(notification_id, current_user.id)
    return NotificationOut.model_validate(notif)


@router.put("/read-all", status_code=status.HTTP_200_OK)
def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    count = service.mark_all_as_read(current_user.id)
    return {"message": f"Marked {count} notifications as read"}
