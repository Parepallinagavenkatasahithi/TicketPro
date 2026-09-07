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
