from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.comment import CommentOut, CommentCreate
from app.services.ticket_service import TicketService
from app.security.rbac import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/tickets/{ticket_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def add_comment(
    ticket_id: int,
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TicketService(db)
    comment = service.add_comment(
        ticket_id=ticket_id,
        author=current_user,
        content=comment_in.content,
        is_internal_note=comment_in.is_internal_note
    )
    return CommentOut(
        id=comment.id,
        ticket_id=comment.ticket_id,
        author_id=comment.author_id,
        author_name=current_user.full_name,
        author_role=current_user.role_name,
        author_avatar=current_user.avatar_url,
        content=comment.content,
        is_internal_note=comment.is_internal_note,
        created_at=comment.created_at,
        updated_at=comment.updated_at
    )
