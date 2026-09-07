from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.approval import ApprovalRequestOut, ApprovalRequestCreate, ApprovalDecisionRequest, ApprovalStepOut
from app.models.approval import ApprovalRequest, ApprovalStep
from app.services.approval_service import ApprovalService
from app.security.rbac import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[ApprovalRequestOut])
def list_approvals(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(ApprovalRequest)
    if current_user.role_name == "EMPLOYEE":
        query = query.filter(ApprovalRequest.requester_id == current_user.id)
    requests = query.order_by(ApprovalRequest.created_at.desc()).all()

    results = []
    for req in requests:
        steps = [
            ApprovalStepOut(
                id=s.id,
                step_number=s.step_number,
                approver_id=s.approver_id,
                approver_name=s.approver.full_name if s.approver else "Approver",
                status=s.status,
                decision_notes=s.decision_notes,
                decided_at=s.decided_at
            ) for s in req.steps
        ]
        results.append(ApprovalRequestOut(
            id=req.id,
            ticket_id=req.ticket_id,
            ticket_number=req.ticket.ticket_number if req.ticket else "N/A",
            requester_id=req.requester_id,
            requester_name=req.requester.full_name if req.requester else "User",
            title=req.title,
            rationale=req.rationale,
            status=req.status,
            created_at=req.created_at,
            steps=steps
        ))
    return results


@router.post("", response_model=ApprovalRequestOut, status_code=status.HTTP_201_CREATED)
def create_approval_request(
    request_in: ApprovalRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ApprovalService(db)
    req = service.create_approval_request(request_in, current_user)
    steps = [
        ApprovalStepOut(
            id=s.id,
            step_number=s.step_number,
            approver_id=s.approver_id,
            approver_name=s.approver.full_name if s.approver else "Approver",
            status=s.status,
            decision_notes=s.decision_notes,
            decided_at=s.decided_at
        ) for s in req.steps
    ]
    return ApprovalRequestOut(
        id=req.id,
        ticket_id=req.ticket_id,
        ticket_number=req.ticket.ticket_number if req.ticket else "N/A",
        requester_id=req.requester_id,
        requester_name=current_user.full_name,
        title=req.title,
        rationale=req.rationale,
        status=req.status,
        created_at=req.created_at,
        steps=steps
    )


@router.put("/steps/{step_id}/decide", response_model=ApprovalStepOut)
def decide_approval_step(
    step_id: int,
    decision_in: ApprovalDecisionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ApprovalService(db)
    step = service.decide_step(step_id, decision_in, current_user)
    return ApprovalStepOut(
        id=step.id,
        step_number=step.step_number,
        approver_id=step.approver_id,
        approver_name=current_user.full_name,
        status=step.status,
        decision_notes=step.decision_notes,
        decided_at=step.decided_at
    )
