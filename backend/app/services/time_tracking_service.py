from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from app.models.time_tracking import TimeEntry
from app.schemas.time_tracking import TimeEntryCreate
from app.models.user import User

class TimeTrackingService:
    def __init__(self, db: Session):
        self.db = db

    def log_time(self, entry_in: TimeEntryCreate, user: User) -> TimeEntry:
        entry = TimeEntry(
            ticket_id=entry_in.ticket_id,
            user_id=user.id,
            hours_spent=entry_in.hours_spent,
            activity_type=entry_in.activity_type.upper(),
            description=entry_in.description,
            logged_at=datetime.now(timezone.utc)
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_entries_for_ticket(self, ticket_id: int) -> List[TimeEntry]:
        return self.db.query(TimeEntry).filter(TimeEntry.ticket_id == ticket_id).order_by(TimeEntry.logged_at.desc()).all()
