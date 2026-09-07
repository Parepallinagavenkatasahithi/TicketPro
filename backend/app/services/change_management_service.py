from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.change_request import ChangeRequest
from app.schemas.change_request import ChangeRequestCreate, ChangeRequestStatusUpdate
from app.models.user import User
from app.core.exceptions import NotFoundError

class ChangeManagementService:
    def __init__(self, db: Session):
        self.db = db

    def create_change_request(self, chg_in: ChangeRequestCreate, requester: User) -> ChangeRequest:
        count = self.db.query(ChangeRequest).count() + 1
        chg_num = f"CHG-2026-{1000 + count}"
        chg = ChangeRequest(
            change_number=chg_num,
            title=chg_in.title,
            description=chg_in.description,
            reason_for_change=chg_in.reason_for_change,
            impact_analysis=chg_in.impact_analysis,
            rollback_plan=chg_in.rollback_plan,
            category=chg_in.category.upper(),
            risk_level=chg_in.risk_level.upper(),
            status="PENDING_APPROVAL",
            requester_id=requester.id,
            assigned_cab_lead_id=chg_in.assigned_cab_lead_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.db.add(chg)
        self.db.commit()
        self.db.refresh(chg)
        return chg

    def list_change_requests(self) -> List[ChangeRequest]:
        return self.db.query(ChangeRequest).order_by(ChangeRequest.created_at.desc()).all()
