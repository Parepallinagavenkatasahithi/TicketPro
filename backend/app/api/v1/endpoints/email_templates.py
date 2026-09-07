from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.email_template import EmailTemplateOut, EmailTemplateCreate
from app.services.email_template_service import EmailTemplateService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[EmailTemplateOut])
def list_email_templates(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = EmailTemplateService(db)
    templates = service.list_templates()
    return [EmailTemplateOut.model_validate(t) for t in templates]

@router.post("", response_model=EmailTemplateOut, status_code=status.HTTP_201_CREATED)
def create_email_template(
    tmpl_in: EmailTemplateCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    service = EmailTemplateService(db)
    t = service.create_template(tmpl_in)
    return EmailTemplateOut.model_validate(t)
