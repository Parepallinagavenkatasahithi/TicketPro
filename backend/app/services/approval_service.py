from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.approval import ApprovalRequest, ApprovalStep, ApprovalStatus
from app.models.ticket import Ticket, TicketStatus, TicketHistory
from app.models.user import User
from app.schemas.approval import ApprovalRequestCreate, ApprovalDecisionRequest
from app.services.notification_service import NotificationService
from app.core.exceptions import NotFoundError, ApprovalError, PermissionDeniedError


class ApprovalService:
    def __init__(self, db: Session):
        self.db = db

    def create_approval_request(self, request_in: ApprovalRequestCreate, requester: User) -> ApprovalRequest:
        ticket = self.db.query(Ticket).filter(Ticket.id == request_in.ticket_id).first()
        if not ticket:
            raise NotFoundError("Ticket", str(request_in.ticket_id))

        approval_req = ApprovalRequest(
            ticket_id=ticket.id,
            requester_id=requester.id,
            title=request_in.title,
            rationale=request_in.rationale,
            status=ApprovalStatus.PENDING.value
        )
        self.db.add(approval_req)
        self.db.flush()

        notif_service = NotificationService(self.db)
        for idx, approver_id in enumerate(request_in.approver_ids, start=1):
            step = ApprovalStep(
                approval_request_id=approval_req.id,
                step_number=idx,
                approver_id=approver_id,
                status=ApprovalStatus.PENDING.value
            )
            self.db.add(step)
            
            notif_service.create_notification(
                user_id=approver_id,
                title="Approval Requested",
                message=f"Approval requested for ticket {ticket.ticket_number}: {request_in.title}",
                notification_type="APPROVAL_REQUIRED",
                reference_id=ticket.ticket_number
            )

        ticket.status = TicketStatus.WAITING_FOR_APPROVAL.value
        history = TicketHistory(
            ticket_id=ticket.id,
            actor_id=requester.id,
            event_type="APPROVAL_REQUESTED",
            new_value=ApprovalStatus.PENDING.value,
            description=f"Approval requested: {request_in.title}"
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(approval_req)
        return approval_req

    def decide_step(self, step_id: int, decision_in: ApprovalDecisionRequest, actor: User) -> ApprovalStep:
        step = self.db.query(ApprovalStep).filter(ApprovalStep.id == step_id).first()
        if not step:
            raise NotFoundError("Approval Step", str(step_id))

        if step.approver_id != actor.id and actor.role_name != "ADMIN":
            raise PermissionDeniedError("You are not designated as the approver for this step")

        now = datetime.now(timezone.utc)
        step.status = decision_in.decision.upper()
        step.decision_notes = decision_in.notes
        step.decided_at = now

        approval_req = step.approval_request
        ticket = approval_req.ticket

        if decision_in.decision.upper() == ApprovalStatus.REJECTED.value:
            approval_req.status = ApprovalStatus.REJECTED.value
            ticket.status = TicketStatus.CANCELLED.value
            history_desc = f"Approval rejected by {actor.full_name}. Rationale: {decision_in.notes or 'None'}"
        else:
            # Check if all steps approved
            all_steps = approval_req.steps
            if all(s.status == ApprovalStatus.APPROVED.value for s in all_steps):
                approval_req.status = ApprovalStatus.APPROVED.value
                ticket.status = TicketStatus.IN_PROGRESS.value
                history_desc = f"Approval fully granted. Approved by {actor.full_name}."
            else:
                history_desc = f"Approval step {step.step_number} approved by {actor.full_name}."

        history = TicketHistory(
            ticket_id=ticket.id,
            actor_id=actor.id,
            event_type="APPROVAL_DECISION",
            old_value=ApprovalStatus.PENDING.value,
            new_value=step.status,
            description=history_desc
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(step)
        return step
