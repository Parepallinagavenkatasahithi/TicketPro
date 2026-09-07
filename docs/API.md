# TicketPro API Specification

## Endpoints Overview

### Authentication & Users
- `POST /api/v1/auth/login` — Authenticate user and issue JWT token.
- `POST /api/v1/auth/register` — Register new employee.
- `GET /api/v1/auth/me` — Fetch current authenticated user.
- `GET /api/v1/users` — List employee directory (filtered by role/dept).

### Ticket Lifecycle
- `GET /api/v1/tickets` — List tickets with full pagination, search, and status filters.
- `POST /api/v1/tickets` — Submit new support ticket.
- `GET /api/v1/tickets/{id}` — Fetch ticket workspace detail.
- `PUT /api/v1/tickets/{id}/status` — Update ticket status (enforces state machine).
- `PUT /api/v1/tickets/{id}/assign` — Assign/reassign ticket agent.
- `POST /api/v1/tickets/{id}/escalate` — Bump ticket priority and trigger escalation event.

### Comments & Attachments
- `POST /api/v1/tickets/{id}/comments` — Add public comment or agent internal note.
- `POST /api/v1/tickets/{id}/attachments` — Upload attachment file.

### SLA & Approvals
- `GET /api/v1/sla/policies` — List SLA policies.
- `GET /api/v1/approvals` — List approval workflow requests.
- `PUT /api/v1/approvals/steps/{id}/decide` — Record approval decision (APPROVED/REJECTED).

### Analytics & Reports
- `GET /api/v1/analytics/dashboard` — Fetch dashboard metrics.
- `GET /api/v1/reports/export/csv` — Export ticket operations CSV report.
