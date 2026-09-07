from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    total_tickets: int
    open_tickets: int
    in_progress_tickets: int
    resolved_tickets: int
    overdue_tickets: int
    
    total_trend_percentage: float = 12.5
    open_trend_percentage: float = -5.2
    in_progress_trend_percentage: float = 8.1
    resolved_trend_percentage: float = 15.3
    overdue_trend_percentage: float = -18.0
    
    sla_compliance_rate: float
    sla_compliant_tickets: int
    sla_total_eligible: int


class TicketTrendPoint(BaseModel):
    date: str  # e.g., "Mon", "Tue", "2026-09-01"
    open: int
    in_progress: int
    resolved: int
    overdue: int


class PriorityDistribution(BaseModel):
    priority: str
    count: int
    percentage: float


class CategoryDistribution(BaseModel):
    category: str
    count: int
    percentage: float


class AgentWorkload(BaseModel):
    agent_id: int
    agent_name: str
    assigned_count: int
    in_progress_count: int
    resolved_count: int
    avg_resolution_hours: float


class DepartmentWorkload(BaseModel):
    department_id: int
    department_name: str
    ticket_count: int
    open_count: int
    overdue_count: int
    sla_compliance_rate: float
