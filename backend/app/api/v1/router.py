from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, departments, tickets, comments,
    attachments, sla, approvals, announcements,
    notifications, knowledge_base, analytics,
    reports, audit, system
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users & Employees"])
api_router.include_router(departments.router, prefix="/departments", tags=["Departments"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["Tickets Core"])
api_router.include_router(comments.router, tags=["Comments & Notes"])
api_router.include_router(attachments.router, tags=["Attachments"])
api_router.include_router(sla.router, prefix="/sla", tags=["SLA Engine"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["Approvals Workflow"])
api_router.include_router(announcements.router, prefix="/announcements", tags=["Announcements"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notification Center"])
api_router.include_router(knowledge_base.router, prefix="/knowledge-base", tags=["Knowledge Base"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics & KPIs"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports & Export"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit Log"])
api_router.include_router(system.router, prefix="/system", tags=["System Settings & Integrations"])
