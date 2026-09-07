from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.audit import AuditLogOut
from app.services.audit_service import AuditService
from app.security.rbac import require_permission
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[AuditLogOut])
def get_audit_logs(
    resource_type: Optional[str] = None,
    action: Optional[str] = None,
    actor_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_permission("audit.view")),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    logs = service.get_logs(resource_type=resource_type, action=action, actor_id=actor_id, skip=skip, limit=limit)
    results = []
    for log in logs:
        results.append(AuditLogOut(
            id=log.id,
            actor_id=log.actor_id,
            actor_name=log.actor.full_name if log.actor else "System",
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            changes_json=log.changes_json,
            ip_address=log.ip_address,
            user_agent=log.user_agent,
            created_at=log.created_at
        ))
    return results
