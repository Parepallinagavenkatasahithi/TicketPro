from datetime import datetime, timedelta, timezone
from typing import Tuple, Optional
from app.models.sla import SLAPolicy

DEFAULT_SLA_TIMES = {
    "CRITICAL": {"first_response_min": 15, "resolution_min": 120},
    "HIGH": {"first_response_min": 30, "resolution_min": 240},
    "MEDIUM": {"first_response_min": 120, "resolution_min": 480},
    "LOW": {"first_response_min": 480, "resolution_min": 1440},
}


def calculate_sla_due_dates(
    created_at: datetime,
    priority: str,
    policy: Optional[SLAPolicy] = None
) -> Tuple[datetime, datetime]:
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
        
    if policy:
        resp_minutes = policy.max_first_response_minutes
        res_minutes = policy.max_resolution_minutes
    else:
        defaults = DEFAULT_SLA_TIMES.get(priority.upper(), DEFAULT_SLA_TIMES["MEDIUM"])
        resp_minutes = defaults["first_response_min"]
        res_minutes = defaults["resolution_min"]

    first_response_due = created_at + timedelta(minutes=resp_minutes)
    resolution_due = created_at + timedelta(minutes=res_minutes)

    return first_response_due, resolution_due


def check_sla_status(
    created_at: datetime,
    first_response_due: Optional[datetime],
    first_responded_at: Optional[datetime],
    resolution_due: Optional[datetime],
    resolved_at: Optional[datetime]
) -> dict:
    now = datetime.now(timezone.utc)
    
    first_resp_breached = False
    if first_response_due:
        if first_response_due.tzinfo is None:
            first_response_due = first_response_due.replace(tzinfo=timezone.utc)
        if first_responded_at:
            if first_responded_at.tzinfo is None:
                first_responded_at = first_responded_at.replace(tzinfo=timezone.utc)
            first_resp_breached = first_responded_at > first_response_due
        else:
            first_resp_breached = now > first_response_due
            
    res_breached = False
    if resolution_due:
        if resolution_due.tzinfo is None:
            resolution_due = resolution_due.replace(tzinfo=timezone.utc)
        if resolved_at:
            if resolved_at.tzinfo is None:
                resolved_at = resolved_at.replace(tzinfo=timezone.utc)
            res_breached = resolved_at > resolution_due
        else:
            res_breached = now > resolution_due

    return {
        "first_response_breached": first_resp_breached,
        "resolution_breached": res_breached,
        "is_overdue": res_breached or (first_resp_breached and not first_responded_at)
    }
