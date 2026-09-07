# TicketPro — Employee Ticket Management & IT Service Operations Platform

TicketPro is an enterprise-grade IT Service Management (ITSM) and Employee Ticket Operations Platform built with **Python (FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic)** on the backend and **TypeScript (React 18, Vite, Tailwind CSS, TanStack Query, Recharts, Lucide React)** on the frontend.

Designed for realistic enterprise operations, TicketPro supports multi-role access control, automated SLA calculation & breach tracking, intelligent agent ticket routing, multi-step approval workflows, internal agent notes privacy controls, file attachment security, real-time analytics, and automated audit logging.

---

## Key Features

- **Authentication & RBAC Security**: JWT token session architecture with role-based permissions (`ADMIN`, `MANAGER`, `AGENT`, `EMPLOYEE`).
- **Ticket Lifecycle & State Machine**: Validated state transitions (`NEW` → `OPEN` → `ASSIGNED` → `IN_PROGRESS` → `WAITING_FOR_USER` → `RESOLVED` → `CLOSED` / `REOPENED`).
- **SLA & Escalation Engine**: Automated first-response and resolution deadline calculation, warning threshold triggers, and priority escalation events.
- **Intelligent Auto-Routing Engine**: Automatic department and agent selection based on category, priority, and real-time workload balancing.
- **Multi-Step Approval Workflows**: Structured approval steps for privilege changes, software requests, and security authorizations.
- **Comments & Internal Notes**: Security-enforced public employee updates vs. agent-only internal notes.
- **Attachment Security**: Safe file uploads with MIME validation, extension whitelisting, file size limits, and path traversal protection.
- **Self-Service Knowledge Base & Announcements**: Searchable KB articles with helpfulness feedback and company-wide announcements.
- **Operations Dashboard & Analytics**: Dynamic metrics, ticket volume trend charts, priority distribution, agent workload metrics, and CSV report export.
- **Audit Logging**: Comprehensive audit trail capturing actor, action, resource, timestamp, and IP.

---

## Tech Stack & Architecture

- **Backend**: Python 3.11+, FastAPI 0.110, SQLAlchemy 2.0 ORM, Pydantic v2, Alembic, Pytest.
- **Frontend**: React 18, TypeScript 5.4, Vite 5.1, Tailwind CSS 3.4, Recharts, Lucide React.
- **Database**: PostgreSQL (Production) / SQLite (Development & Testing).
- **DevOps**: Docker, Docker Compose, GitHub Actions CI/CD.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm
- Git

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Seed Database
```bash
python scripts/seed_data.py
```
*This populates SQLite database with 104 realistic enterprise tickets, 20+ users, departments, SLA policies, and KB articles.*

### 3. Run Backend API Server
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
*API Swagger Documentation will be available at `http://localhost:8000/docs`.*

### 4. Frontend Setup & Run
```bash
cd frontend
npm install
npm run dev
```
*Open `http://localhost:5173` in your browser.*

---

## Demo Login Credentials

| Role | Email | Password |
|---|---|---|
| **Admin** | `admin@ticketpro.internal` | `Password123!` |
| **IT Manager** | `it.manager@ticketpro.internal` | `Password123!` |
| **Support Agent** | `agent.alex@ticketpro.internal` | `Password123!` |
| **Employee** | `rohit.sharma@ticketpro.internal` | `Password123!` |

---

## Running Tests & Audits

### Run Pytest Test Suite
```bash
python -m pytest --cov=backend/app --cov-report=term-missing tests/backend
```

### Run E2E Full Ticket Lifecycle Test
```bash
python -m pytest tests/e2e/test_full_ticket_lifecycle.py
```

### Run Project Audit
```bash
python scripts/project_audit.py
```

---

## Docker Deployment

To launch the full stack with PostgreSQL, Redis, FastAPI, and Frontend Nginx via Docker Compose:
```bash
docker-compose up --build
```
