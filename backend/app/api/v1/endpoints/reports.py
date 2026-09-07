from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.report_service import ReportService
from app.security.rbac import require_permission
from app.models.user import User

router = APIRouter()


@router.get("/export/csv")
def export_csv_report(
    current_user: User = Depends(require_permission("reports.view")),
    db: Session = Depends(get_db)
):
    service = ReportService(db)
    csv_data = service.generate_csv_report()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ticketpro_report.csv"}
    )
