from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)  # e.g., "ticket.create"
    description = Column(String(255), nullable=True)
    category = Column(String(50), nullable=False, default="general")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)  # EMPLOYEE, AGENT, MANAGER, ADMIN
    description = Column(String(255), nullable=True)
    is_system = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")
    users = relationship("User", back_populates="role_rel")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)  # EMP-1001
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    job_title = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role_name = Column(String(50), nullable=False, default="EMPLOYEE")
    
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    role_rel = relationship("Role", back_populates="users")
    department = relationship("Department", back_populates="members", foreign_keys=[department_id])
    
    requested_tickets = relationship("Ticket", foreign_keys="[Ticket.requester_id]", back_populates="requester")
    assigned_tickets = relationship("Ticket", foreign_keys="[Ticket.assigned_agent_id]", back_populates="assigned_agent")
    comments = relationship("TicketComment", back_populates="author")
    audit_logs = relationship("AuditLog", back_populates="actor")
