from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.time_tracking import TimeEntryOut, TimeEntryCreate
from app.services.time_tracking_service import TimeTrackingService
from app.security.rbac import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/tickets/{ticket_id}", response_model=List[TimeEntryOut])
def get_time_entries(ticket_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = TimeTrackingService(db)
    entries = service.get_entries_for_ticket(ticket_id)
    results = []
    for e in entries:
        results.append(TimeEntryOut(
            id=e.id,
            ticket_id=e.ticket_id,
            ticket_number=e.ticket.ticket_number if e.ticket else "N/A",
            user_id=e.user_id,
            user_name=e.user.full_name if e.user else "User",
            hours_spent=e.hours_spent,
            activity_type=e.activity_type,
            description=e.description,
            logged_at=e.logged_at
        ))
    return results

@router.post("", response_model=TimeEntryOut, status_code=status.HTTP_201_CREATED)
def log_time(
    entry_in: TimeEntryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TimeTrackingService(db)
    e = service.log_time(entry_in, current_user)
    return TimeEntryOut.model_validate(e)
