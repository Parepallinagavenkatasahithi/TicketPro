from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.core.exceptions import NotFoundError


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def create_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: str,
        reference_id: Optional[str] = None
    ) -> Notification:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            reference_id=reference_id,
            is_read=False,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(notif)
        self.db.commit()
        self.db.refresh(notif)
        return notif

    def get_user_notifications(self, user_id: int, unread_only: bool = False, limit: int = 50) -> List[Notification]:
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(Notification.created_at.desc()).limit(limit).all()

    def mark_as_read(self, notification_id: int, user_id: int) -> Notification:
        notif = self.db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        if not notif:
            raise NotFoundError("Notification", str(notification_id))

        notif.is_read = True
        notif.read_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(notif)
        return notif

    def mark_all_as_read(self, user_id: int) -> int:
        now = datetime.now(timezone.utc)
        updated = self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True, "read_at": now})
        self.db.commit()
        return updated
