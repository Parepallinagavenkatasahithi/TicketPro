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

    def list_surveys(self) -> List[SurveyResponse]:
        return self.db.query(SurveyResponse).order_by(SurveyResponse.created_at.desc()).all()
