from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from app.models.user import User


class AuditService:
    def __init__(self, db: Session):
        self.db = db

    def log_event(
        self,
        action: str,
        resource_type: str,
        actor_id: Optional[int] = None,
        resource_id: Optional[str] = None,
        changes_json: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        log = AuditLog(
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes_json=changes_json,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_logs(
        self,
        resource_type: Optional[str] = None,
        action: Optional[str] = None,
        actor_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        query = self.db.query(AuditLog)
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type.upper())
        if action:
            query = query.filter(AuditLog.action == action.upper())
        if actor_id:
            query = query.filter(AuditLog.actor_id == actor_id)

        return query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
