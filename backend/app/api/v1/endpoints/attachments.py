import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.core.exceptions import AttachmentError, NotFoundError
from app.schemas.attachment import AttachmentOut
from app.models.ticket import Ticket, TicketAttachment
from app.models.user import User
from app.security.rbac import get_current_user

router = APIRouter()


@router.post("/tickets/{ticket_id}/attachments", response_model=AttachmentOut, status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    ticket_id: int,
    file: UploadFile = File(...),
    comment_id: int = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise NotFoundError("Ticket", str(ticket_id))

    # Sanitize and validate file extension (Section 24, 63)
    original_filename = os.path.basename(file.filename)
    if not original_filename:
        raise AttachmentError("Invalid filename provided")

    ext = original_filename.rsplit(".", 1)[-1].lower() if "." in original_filename else ""
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise AttachmentError(f"File extension '.{ext}' is not allowed")

    # Read and check size
    content = await file.read()
    file_size = len(content)
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        raise AttachmentError(f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB")

    # Generate random UUID storage identifier (path traversal protection)
    safe_storage_name = f"{uuid.uuid4().hex}.{ext}"
    storage_dir = settings.UPLOAD_DIR
    os.makedirs(storage_dir, exist_ok=True)
    full_path = os.path.join(storage_dir, safe_storage_name)

    with open(full_path, "wb") as f:
        f.write(content)

    attachment = TicketAttachment(
        ticket_id=ticket.id,
        comment_id=comment_id,
        uploader_id=current_user.id,
        file_name=original_filename,
        storage_path=f"/uploads/{safe_storage_name}",
        file_size=file_size,
        mime_type=file.content_type or "application/octet-stream"
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return AttachmentOut(
        id=attachment.id,
        ticket_id=attachment.ticket_id,
        comment_id=attachment.comment_id,
        uploader_id=attachment.uploader_id,
        uploader_name=current_user.full_name,
        file_name=attachment.file_name,
        storage_path=attachment.storage_path,
        file_size=attachment.file_size,
        mime_type=attachment.mime_type,
        created_at=attachment.created_at
    )
