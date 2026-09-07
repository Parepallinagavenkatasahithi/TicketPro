from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.analytics import (
    DashboardMetrics, TicketTrendPoint, PriorityDistribution, AgentWorkload
)
from app.services.report_service import ReportService
from app.security.rbac import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/dashboard", response_model=DashboardMetrics)
def get_dashboard_metrics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ReportService(db)
    return service.get_dashboard_metrics(current_user=current_user)


@router.get("/trends", response_model=List[TicketTrendPoint])
def get_ticket_trends(days: int = 7, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ReportService(db)
    return service.get_ticket_trends(days=days)


@router.get("/priorities", response_model=List[PriorityDistribution])
def get_priority_distribution(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ReportService(db)
    return service.get_priority_distribution()


@router.get("/agents/workload", response_model=List[AgentWorkload])
def get_agent_workloads(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ReportService(db)
    return service.get_agent_workloads()
