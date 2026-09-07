from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, departments, tickets, comments,
    attachments, sla, approvals, announcements,
    notifications, knowledge_base, analytics,
    reports, audit, system, assets, change_requests,
    problems, surveys, time_tracking, vendors,
    contracts, on_call, service_catalog, custom_fields,
    email_templates
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
api_router.include_router(assets.router, prefix="/assets", tags=["Asset Management"])
api_router.include_router(change_requests.router, prefix="/change-requests", tags=["Change Management"])
api_router.include_router(problems.router, prefix="/problems", tags=["Problem Management"])
api_router.include_router(surveys.router, prefix="/surveys", tags=["CSAT Surveys"])
api_router.include_router(time_tracking.router, prefix="/time-tracking", tags=["Time Tracking"])
api_router.include_router(vendors.router, prefix="/vendors", tags=["Vendor & Software Licenses"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["Contracts & SLA Maintenance"])
api_router.include_router(on_call.router, prefix="/on-call", tags=["On-Call Roster"])
api_router.include_router(service_catalog.router, prefix="/service-catalog", tags=["Service Catalog"])
api_router.include_router(custom_fields.router, prefix="/custom-fields", tags=["Custom Fields Engine"])
api_router.include_router(email_templates.router, prefix="/email-templates", tags=["Email Notification Templates"])
