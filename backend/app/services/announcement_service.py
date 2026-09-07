from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.announcement import Announcement, AnnouncementStatus, AnnouncementPriority
from app.models.user import User
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate
from app.services.notification_service import NotificationService
from app.core.exceptions import NotFoundError


class AnnouncementService:
    def __init__(self, db: Session):
        self.db = db

    def list_announcements(
        self,
        current_user: Optional[User] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Announcement]:
        query = self.db.query(Announcement)
        if status:
            query = query.filter(Announcement.status == status.upper())
        elif current_user and current_user.role_name == "EMPLOYEE":
            query = query.filter(Announcement.status == AnnouncementStatus.PUBLISHED.value)

        return query.order_by(Announcement.created_at.desc()).limit(limit).all()

    def create_announcement(self, announcement_in: AnnouncementCreate, author: User) -> Announcement:
        now = datetime.now(timezone.utc)
        pub_at = now if announcement_in.status.upper() == AnnouncementStatus.PUBLISHED.value else None

        announcement = Announcement(
            title=announcement_in.title,
            content=announcement_in.content,
            priority=announcement_in.priority.upper(),
            target_audience=announcement_in.target_audience.upper(),
            status=announcement_in.status.upper(),
            author_id=author.id,
            published_at=pub_at,
            scheduled_for=announcement_in.scheduled_for,
            created_at=now,
            updated_at=now
        )
        self.db.add(announcement)
        self.db.commit()
        self.db.refresh(announcement)

        # Notify users if published
        if announcement.status == AnnouncementStatus.PUBLISHED.value:
            notif_service = NotificationService(self.db)
            users = self.db.query(User).filter(User.is_active == True).all()
            for u in users:
                notif_service.create_notification(
                    user_id=u.id,
                    title=f"ANNOUNCEMENT: {announcement.title}",
                    message=announcement.content[:150] + "...",
                    notification_type="ANNOUNCEMENT",
                    reference_id=str(announcement.id)
                )

        return announcement
