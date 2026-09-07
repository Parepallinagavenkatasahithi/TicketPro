import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Generated: {path}")

# 1. Schemas
write("backend/app/schemas/asset.py", """
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AssetOut(BaseModel):
    id: int
    asset_tag: str
    name: str
    category: str
    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    status: str
    assigned_to_user_id: Optional[int] = None
    assigned_to_user_name: Optional[str] = None
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    location: Optional[str] = None
    purchase_date: Optional[datetime] = None
    warranty_expiry_date: Optional[datetime] = None
    purchase_cost: Optional[float] = None
    vendor_name: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AssetCreate(BaseModel):
    asset_tag: str
    name: str
    category: str
    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    status: str = "IN_USE"
    assigned_to_user_id: Optional[int] = None
    department_id: Optional[int] = None
    location: Optional[str] = None
    purchase_cost: Optional[float] = None
    vendor_name: Optional[str] = None
    notes: Optional[str] = None

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    assigned_to_user_id: Optional[int] = None
    department_id: Optional[int] = None
    location: Optional[str] = None
    notes: Optional[str] = None
""")

write("backend/app/schemas/change_request.py", """
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ChangeRequestOut(BaseModel):
    id: int
    change_number: str
    title: str
    description: str
    reason_for_change: str
    impact_analysis: str
    rollback_plan: str
    category: str
    risk_level: str
    status: str
    requester_id: int
    requester_name: Optional[str] = None
    assigned_cab_lead_id: Optional[int] = None
    assigned_cab_lead_name: Optional[str] = None
    scheduled_start_at: Optional[datetime] = None
    scheduled_end_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChangeRequestCreate(BaseModel):
    title: str
    description: str
    reason_for_change: str
    impact_analysis: str
    rollback_plan: str
    category: str = "STANDARD"
    risk_level: str = "MEDIUM"
    assigned_cab_lead_id: Optional[int] = None

class ChangeRequestStatusUpdate(BaseModel):
    status: str
    decision_notes: Optional[str] = None
""")

write("backend/app/schemas/problem.py", """
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ProblemOut(BaseModel):
    id: int
    problem_number: str
    title: str
    description: str
    root_cause: Optional[str] = None
    workaround: Optional[str] = None
    status: str
    impact: str
    owner_id: int
    owner_name: Optional[str] = None
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProblemCreate(BaseModel):
    title: str
    description: str
    root_cause: Optional[str] = None
    workaround: Optional[str] = None
    impact: str = "MEDIUM"
    department_id: Optional[int] = None
""")

write("backend/app/schemas/survey.py", """
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SurveyOut(BaseModel):
    id: int
    ticket_id: int
    ticket_number: Optional[str] = None
    respondent_id: int
    respondent_name: Optional[str] = None
    rating: int
    feedback_text: Optional[str] = None
    agent_id: Optional[int] = None
    agent_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SurveyCreate(BaseModel):
    ticket_id: int
    rating: int
    feedback_text: Optional[str] = None
""")

write("backend/app/schemas/time_tracking.py", """
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TimeEntryOut(BaseModel):
    id: int
    ticket_id: int
    ticket_number: Optional[str] = None
    user_id: int
    user_name: Optional[str] = None
    hours_spent: float
    activity_type: str
    description: Optional[str] = None
    logged_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TimeEntryCreate(BaseModel):
    ticket_id: int
    hours_spent: float
    activity_type: str = "RESEARCH"
    description: Optional[str] = None
""")

# 2. Services
write("backend/app/services/asset_service.py", """
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate
from app.core.exceptions import NotFoundError, ValidationError

class AssetService:
    def __init__(self, db: Session):
        self.db = db

    def list_assets(self, category: Optional[str] = None, status: Optional[str] = None, search: Optional[str] = None) -> List[Asset]:
        query = self.db.query(Asset)
        if category:
            query = query.filter(Asset.category == category.upper())
        if status:
            query = query.filter(Asset.status == status.upper())
        if search:
            pattern = f"%{search}%"
            query = query.filter((Asset.asset_tag.ilike(pattern)) | (Asset.name.ilike(pattern)))
        return query.order_by(Asset.created_at.desc()).all()

    def create_asset(self, asset_in: AssetCreate) -> Asset:
        existing = self.db.query(Asset).filter(Asset.asset_tag == asset_in.asset_tag).first()
        if existing:
            raise ValidationError(f"Asset tag '{asset_in.asset_tag}' already exists")
        asset = Asset(
            asset_tag=asset_in.asset_tag,
            name=asset_in.name,
            category=asset_in.category.upper(),
            model_number=asset_in.model_number,
            serial_number=asset_in.serial_number,
            status=asset_in.status.upper(),
            assigned_to_user_id=asset_in.assigned_to_user_id,
            department_id=asset_in.department_id,
            location=asset_in.location,
            purchase_cost=asset_in.purchase_cost,
            vendor_name=asset_in.vendor_name,
            notes=asset_in.notes,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset
""")

write("backend/app/services/change_management_service.py", """
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
""")

write("backend/app/services/problem_management_service.py", """
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.problem import Problem
from app.schemas.problem import ProblemCreate
from app.models.user import User

class ProblemManagementService:
    def __init__(self, db: Session):
        self.db = db

    def create_problem(self, prb_in: ProblemCreate, owner: User) -> Problem:
        count = self.db.query(Problem).count() + 1
        prb_num = f"PRB-2026-{1000 + count}"
        prb = Problem(
            problem_number=prb_num,
            title=prb_in.title,
            description=prb_in.description,
            root_cause=prb_in.root_cause,
            workaround=prb_in.workaround,
            status="INVESTIGATING",
            impact=prb_in.impact.upper(),
            owner_id=owner.id,
            department_id=prb_in.department_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.db.add(prb)
        self.db.commit()
        self.db.refresh(prb)
        return prb

    def list_problems() -> List[Problem]:
        return self.db.query(Problem).order_by(Problem.created_at.desc()).all()
""")

write("backend/app/services/survey_service.py", """
from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from app.models.survey import SurveyResponse
from app.schemas.survey import SurveyCreate
from app.models.ticket import Ticket
from app.models.user import User

class SurveyService:
    def __init__(self, db: Session):
        self.db = db

    def submit_survey(self, survey_in: SurveyCreate, respondent: User) -> SurveyResponse:
        ticket = self.db.query(Ticket).filter(Ticket.id == survey_in.ticket_id).first()
        res = SurveyResponse(
            ticket_id=survey_in.ticket_id,
            respondent_id=respondent.id,
            rating=survey_in.rating,
            feedback_text=survey_in.feedback_text,
            agent_id=ticket.assigned_agent_id if ticket else None,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(res)
        self.db.commit()
        self.db.refresh(res)
        return res

    def list_surveys() -> List[SurveyResponse]:
        return self.db.query(SurveyResponse).order_by(SurveyResponse.created_at.desc()).all()
""")

write("backend/app/services/time_tracking_service.py", """
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
""")

# 3. Endpoints
write("backend/app/api/v1/endpoints/assets.py", """
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.asset import AssetOut, AssetCreate, AssetUpdate
from app.services.asset_service import AssetService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[AssetOut])
def list_assets(
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    assets = service.list_assets(category=category, status=status, search=search)
    results = []
    for a in assets:
        results.append(AssetOut(
            id=a.id,
            asset_tag=a.asset_tag,
            name=a.name,
            category=a.category,
            model_number=a.model_number,
            serial_number=a.serial_number,
            status=a.status,
            assigned_to_user_id=a.assigned_to_user_id,
            assigned_to_user_name=a.assigned_user.full_name if a.assigned_user else None,
            department_id=a.department_id,
            department_name=a.department.name if a.department else None,
            location=a.location,
            purchase_date=a.purchase_date,
            warranty_expiry_date=a.warranty_expiry_date,
            purchase_cost=a.purchase_cost,
            vendor_name=a.vendor_name,
            notes=a.notes,
            created_at=a.created_at,
            updated_at=a.updated_at
        ))
    return results

@router.post("", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
def create_asset(
    asset_in: AssetCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    a = service.create_asset(asset_in)
    return AssetOut.model_validate(a)
""")

write("backend/app/api/v1/endpoints/change_requests.py", """
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.change_request import ChangeRequestOut, ChangeRequestCreate
from app.services.change_management_service import ChangeManagementService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[ChangeRequestOut])
def list_change_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ChangeManagementService(db)
    chgs = service.list_change_requests()
    results = []
    for c in chgs:
        results.append(ChangeRequestOut(
            id=c.id,
            change_number=c.change_number,
            title=c.title,
            description=c.description,
            reason_for_change=c.reason_for_change,
            impact_analysis=c.impact_analysis,
            rollback_plan=c.rollback_plan,
            category=c.category,
            risk_level=c.risk_level,
            status=c.status,
            requester_id=c.requester_id,
            requester_name=c.requester.full_name if c.requester else "User",
            assigned_cab_lead_id=c.assigned_cab_lead_id,
            assigned_cab_lead_name=c.cab_lead.full_name if c.cab_lead else None,
            scheduled_start_at=c.scheduled_start_at,
            scheduled_end_at=c.scheduled_end_at,
            created_at=c.created_at,
            updated_at=c.updated_at
        ))
    return results

@router.post("", response_model=ChangeRequestOut, status_code=status.HTTP_201_CREATED)
def create_change_request(
    chg_in: ChangeRequestCreate,
    current_user: User = Depends(require_permission("ticket.create")),
    db: Session = Depends(get_db)
):
    service = ChangeManagementService(db)
    c = service.create_change_request(chg_in, current_user)
    return ChangeRequestOut.model_validate(c)
""")

write("backend/app/api/v1/endpoints/problems.py", """
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.problem import ProblemOut, ProblemCreate
from app.services.problem_management_service import ProblemManagementService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[ProblemOut])
def list_problems(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ProblemManagementService(db)
    prbs = service.list_problems()
    results = []
    for p in prbs:
        results.append(ProblemOut(
            id=p.id,
            problem_number=p.problem_number,
            title=p.title,
            description=p.description,
            root_cause=p.root_cause,
            workaround=p.workaround,
            status=p.status,
            impact=p.impact,
            owner_id=p.owner_id,
            owner_name=p.owner.full_name if p.owner else "Owner",
            department_id=p.department_id,
            department_name=p.department.name if p.department else None,
            resolved_at=p.resolved_at,
            created_at=p.created_at
        ))
    return results

@router.post("", response_model=ProblemOut, status_code=status.HTTP_201_CREATED)
def create_problem(
    prb_in: ProblemCreate,
    current_user: User = Depends(require_permission("ticket.create")),
    db: Session = Depends(get_db)
):
    service = ProblemManagementService(db)
    p = service.create_problem(prb_in, current_user)
    return ProblemOut.model_validate(p)
""")

write("backend/app/api/v1/endpoints/surveys.py", """
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.survey import SurveyOut, SurveyCreate
from app.services.survey_service import SurveyService
from app.security.rbac import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[SurveyOut])
def list_surveys(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = SurveyService(db)
    surveys = service.list_surveys()
    results = []
    for s in surveys:
        results.append(SurveyOut(
            id=s.id,
            ticket_id=s.ticket_id,
            ticket_number=s.ticket.ticket_number if s.ticket else "N/A",
            respondent_id=s.respondent_id,
            respondent_name=s.respondent.full_name if s.respondent else "User",
            rating=s.rating,
            feedback_text=s.feedback_text,
            agent_id=s.agent_id,
            agent_name=s.agent.full_name if s.agent else None,
            created_at=s.created_at
        ))
    return results

@router.post("", response_model=SurveyOut, status_code=status.HTTP_201_CREATED)
def submit_survey(
    survey_in: SurveyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = SurveyService(db)
    s = service.submit_survey(survey_in, current_user)
    return SurveyOut.model_validate(s)
""")

write("backend/app/api/v1/endpoints/time_tracking.py", """
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
""")

print("All new backend models, schemas, services, and endpoints written!")
