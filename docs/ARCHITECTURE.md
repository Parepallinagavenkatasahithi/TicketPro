# TicketPro Architecture Specification

## Overview
TicketPro is structured as a decoupled multi-tier full-stack application.

```
[ Client Layer ]  React 18 + TypeScript SPA (Vite + Tailwind)
       │
       ▼
[ API Layer ]     FastAPI REST API V1 + OpenAPI Specs
       │
       ▼
[ Domain Layer ]  State Machine, SLA Engine, Workload Balancer, RBAC Guard
       │
       ▼
[ Service Layer]  Auth, Ticket, User, SLA, Approval, Audit Services
       │
       ▼
[ Data Layer ]    SQLAlchemy 2.0 ORM + Alembic + PostgreSQL/SQLite
```

## Layer Responsibilities
1. **API Layer (`app/api/v1/endpoints`)**: Route handling, request validation via Pydantic schemas, dependency injection.
2. **Security & RBAC (`app/security/rbac.py`)**: Permission checks, JWT decoding, user context injection.
3. **Domain Layer (`app/domain/`)**: Pure business logic (State machine transitions, SLA target calculators).
4. **Service Layer (`app/services/`)**: Orchestrating database transactions, logging audit trails, dispatching notifications.
5. **Data Layer (`app/models/`)**: Declarative SQLAlchemy models.
