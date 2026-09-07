from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from app.models.email_template import EmailTemplate
from app.schemas.email_template import EmailTemplateCreate


class EmailTemplateService:
    def __init__(self, db: Session):
        self.db = db

    def list_templates(self) -> List[EmailTemplate]:
        return self.db.query(EmailTemplate).filter(EmailTemplate.is_active == True).all()

    def create_template(self, tmpl_in: EmailTemplateCreate) -> EmailTemplate:
        tmpl = EmailTemplate(**tmpl_in.model_dump())
        self.db.add(tmpl)
        self.db.commit()
        self.db.refresh(tmpl)
        return tmpl
