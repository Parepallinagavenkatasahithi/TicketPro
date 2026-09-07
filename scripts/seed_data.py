import sys
import os
from datetime import datetime, timedelta, timezone

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, Role, Permission, RolePermission
from app.models.department import Department
from app.models.ticket import Ticket, TicketCategory, TicketComment, TicketAttachment, TicketHistory, TicketStatus, TicketPriority
from app.models.sla import SLAPolicy, SLABreach
from app.models.announcement import Announcement, AnnouncementPriority, AnnouncementStatus
from app.models.knowledge_base import KnowledgeBaseArticle
from app.models.notification import Notification
from app.models.audit import AuditLog
from app.models.system import SystemSetting, Integration

def seed_database():
    print("Initializing Database Schema...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).count() > 0:
            print("Database already contains records. Skipping seed.")
            return

        print("Seeding Roles and Permissions...")
        roles_data = [
            ("ADMIN", "System Administrator with full access"),
            ("MANAGER", "Department Manager overseeing team tickets and SLA compliance"),
            ("AGENT", "Support Agent handling ticket queues and resolution"),
            ("EMPLOYEE", "Regular Employee submitting tickets and accessing Knowledge Base")
        ]
        roles_map = {}
        for name, desc in roles_data:
            role = Role(name=name, description=desc, is_system=True)
            db.add(role)
            db.flush()
            roles_map[name] = role

        print("Seeding Departments...")
        depts_data = [
            ("Information Technology", "IT", "Core IT infrastructure, hardware, and service desk"),
            ("Human Resources", "HR", "Employee onboarding, payroll, and workplace policies"),
            ("Finance & Accounting", "FIN", "Financial systems, expenses, and procurement"),
            ("Engineering", "ENG", "Software engineering, DevOps, and cloud services"),
            ("Operations", "OPS", "Business operations and logistics"),
            ("Facilities", "FAC", "Office space, physical security, and building management"),
            ("Information Security", "SEC", "Cybersecurity, compliance, and access governance")
        ]
        depts_map = {}
        for name, code, desc in depts_data:
            dept = Department(name=name, code=code, description=desc)
            db.add(dept)
            db.flush()
            depts_map[code] = dept

        print("Seeding SLA Policies...")
        sla_policies = [
            SLAPolicy(name="Critical Priority SLA", priority="CRITICAL", max_first_response_minutes=15, max_resolution_minutes=120, warning_threshold_percent=80.0, is_default=False),
            SLAPolicy(name="High Priority SLA", priority="HIGH", max_first_response_minutes=30, max_resolution_minutes=240, warning_threshold_percent=80.0, is_default=False),
            SLAPolicy(name="Medium Priority SLA", priority="MEDIUM", max_first_response_minutes=120, max_resolution_minutes=480, warning_threshold_percent=80.0, is_default=True),
            SLAPolicy(name="Low Priority SLA", priority="LOW", max_first_response_minutes=480, max_resolution_minutes=1440, warning_threshold_percent=80.0, is_default=False)
        ]
        db.add_all(sla_policies)
        db.flush()

        print("Seeding Ticket Categories...")
        categories_data = [
            ("Hardware", "Laptops, monitors, peripherals, and desk equipment", "MEDIUM", "IT", "Laptop"),
            ("Software", "SaaS subscriptions, operating systems, and dev tools", "MEDIUM", "IT", "Code"),
            ("Network & VPN", "Wi-Fi connectivity, VPN access, and firewall issues", "HIGH", "IT", "Wifi"),
            ("Email & Identity", "Email access, OAuth login, and password resets", "HIGH", "SEC", "Mail"),
            ("Access & Permissions", "Access requests for AWS, GitHub, Jira, and internal tools", "HIGH", "SEC", "Key"),
            ("Security Incident", "Suspicious emails, phishing, or security alerts", "CRITICAL", "SEC", "ShieldAlert"),
            ("HR & Payroll", "Payroll queries, benefits, and HR documentation", "MEDIUM", "HR", "Users"),
            ("Facilities & Office", "Desk setup, HVAC, badge access, and office repairs", "LOW", "FAC", "Building"),
            ("General Other", "Miscellaneous support inquiries", "LOW", "IT", "HelpCircle")
        ]
        categories_map = {}
        for name, desc, prio, dept_code, icon in categories_data:
            cat = TicketCategory(
                name=name,
                description=desc,
                default_priority=prio,
                default_department_id=depts_map[dept_code].id,
                icon_name=icon
            )
            db.add(cat)
            db.flush()
            categories_map[name] = cat

        print("Seeding Users...")
        pwd_hash = get_password_hash("Password123!")

        # Admin user
        admin = User(
            employee_id="EMP-1000",
            email="admin@ticketpro.internal",
            hashed_password=pwd_hash,
            full_name="Sarah Jenkins",
            job_title="VP of Infrastructure & Security",
            phone="+1 (555) 019-2831",
            role_id=roles_map["ADMIN"].id,
            role_name="ADMIN",
            department_id=depts_map["IT"].id,
            is_active=True
        )
        db.add(admin)
        db.flush()

        # Managers
        mgr_it = User(employee_id="EMP-1001", email="it.manager@ticketpro.internal", hashed_password=pwd_hash, full_name="David Miller", job_title="IT Service Desk Manager", role_id=roles_map["MANAGER"].id, role_name="MANAGER", department_id=depts_map["IT"].id)
        mgr_sec = User(employee_id="EMP-1002", email="sec.manager@ticketpro.internal", hashed_password=pwd_hash, full_name="Elena Rostova", job_title="Chief Information Security Officer", role_id=roles_map["MANAGER"].id, role_name="MANAGER", department_id=depts_map["SEC"].id)
        db.add_all([mgr_it, mgr_sec])
        db.flush()
        depts_map["IT"].manager_id = mgr_it.id
        depts_map["SEC"].manager_id = mgr_sec.id

        # Agents
        agents = [
            User(employee_id="EMP-1003", email="agent.alex@ticketpro.internal", hashed_password=pwd_hash, full_name="Alex Rivera", job_title="Senior IT Support Specialist", role_id=roles_map["AGENT"].id, role_name="AGENT", department_id=depts_map["IT"].id),
            User(employee_id="EMP-1004", email="agent.jordan@ticketpro.internal", hashed_password=pwd_hash, full_name="Jordan Chen", job_title="Network & Systems Engineer", role_id=roles_map["AGENT"].id, role_name="AGENT", department_id=depts_map["IT"].id),
            User(employee_id="EMP-1005", email="agent.priya@ticketpro.internal", hashed_password=pwd_hash, full_name="Priya Sharma", job_title="Cybersecurity Analyst", role_id=roles_map["AGENT"].id, role_name="AGENT", department_id=depts_map["SEC"].id),
            User(employee_id="EMP-1006", email="agent.marcus@ticketpro.internal", hashed_password=pwd_hash, full_name="Marcus Vance", job_title="Hardware & Support Specialist", role_id=roles_map["AGENT"].id, role_name="AGENT", department_id=depts_map["IT"].id),
            User(employee_id="EMP-1007", email="agent.sophia@ticketpro.internal", hashed_password=pwd_hash, full_name="Sophia Taylor", job_title="HR Operations Specialist", role_id=roles_map["AGENT"].id, role_name="AGENT", department_id=depts_map["HR"].id)
        ]
        db.add_all(agents)
        db.flush()

        # Employees
        employees = []
        employee_names = [
            ("Rohit Sharma", "Software Engineer", "ENG"),
            ("Emily Watson", "Financial Analyst", "FIN"),
            ("Michael Chang", "Product Manager", "OPS"),
            ("Jessica Taylor", "UX Designer", "ENG"),
            ("Daniel Kim", "Accountant", "FIN"),
            ("Amanda Lopez", "HR Coordinator", "HR"),
            ("James Wilson", "DevOps Engineer", "ENG"),
            ("Rachel Green", "Marketing Lead", "OPS"),
            ("Carlos Mendez", "Office Administrator", "FAC"),
            ("Hannah Abbott", "QA Specialist", "ENG"),
            ("Vikram Patel", "Data Scientist", "ENG"),
            ("Samantha Reed", "Sales Executive", "OPS"),
            ("Liam O'Connor", "SecOps Analyst", "SEC"),
            ("Zoe Martinez", "Talent Acquisition", "HR"),
            ("Oliver Wright", "Legal Counsel", "OPS")
        ]

        for idx, (name, title, dept_code) in enumerate(employee_names, start=8):
            emp = User(
                employee_id=f"EMP-10{idx:02d}",
                email=f"{name.lower().replace(' ', '.')}@ticketpro.internal",
                hashed_password=pwd_hash,
                full_name=name,
                job_title=title,
                role_id=roles_map["EMPLOYEE"].id,
                role_name="EMPLOYEE",
                department_id=depts_map[dept_code].id
            )
            employees.append(emp)

        db.add_all(employees)
        db.flush()

        print("Seeding 100+ Enterprise Tickets...")
        sample_ticket_titles = [
            ("Unable to connect to Corporate VPN from remote location", "Network & VPN", "HIGH", "IT"),
            ("MacBook Pro M3 battery draining rapidly during Zoom calls", "Hardware", "MEDIUM", "IT"),
            ("Request AWS Admin Access for Staging Deployment", "Access & Permissions", "HIGH", "SEC"),
            ("Suspicious Phishing Email received from unknown external domain", "Security Incident", "CRITICAL", "SEC"),
            ("Docker Desktop license key expired on Windows Workstation", "Software", "MEDIUM", "IT"),
            ("Monitors in Conference Room 4B not displaying HDMI output", "Facilities & Office", "LOW", "FAC"),
            ("Direct Deposit bank account update for upcoming payroll cycle", "HR & Payroll", "MEDIUM", "HR"),
            ("GitLab CI/CD runner timing out on release pipeline", "Software", "HIGH", "IT"),
            ("Password reset required for SSO Active Directory account", "Email & Identity", "HIGH", "SEC"),
            ("Standing desk height controller malfunctioning in Pod C", "Facilities & Office", "LOW", "FAC"),
            ("VS Code remote SSH extension failing connection to dev server", "Software", "MEDIUM", "IT"),
            ("Request 4K External Display for Graphic Design Workstation", "Hardware", "MEDIUM", "IT"),
            ("Wi-Fi network disconnecting repeatedly on 5th Floor", "Network & VPN", "HIGH", "IT"),
            ("Quarterly Tax Statement document download error in HR Portal", "HR & Payroll", "MEDIUM", "HR"),
            ("Potential malware alert flagged on Endpoint Protection agent", "Security Incident", "CRITICAL", "SEC")
        ]

        statuses = [TicketStatus.OPEN.value, TicketStatus.IN_PROGRESS.value, TicketStatus.WAITING_FOR_USER.value, TicketStatus.RESOLVED.value, TicketStatus.CLOSED.value]
        now = datetime.now(timezone.utc)

        tickets_created = 0
        for i in range(1, 105):
            title_tpl, cat_name, prio, dept_code = sample_ticket_titles[i % len(sample_ticket_titles)]
            req_user = employees[i % len(employees)]
            assigned_agent = agents[i % len(agents)] if i % 4 != 0 else None
            status_val = statuses[i % len(statuses)]
            
            created_days_ago = (105 - i) // 4
            created_at = now - timedelta(days=created_days_ago, hours=(i % 12))
            resp_due = created_at + timedelta(minutes=30)
            res_due = created_at + timedelta(hours=4)

            is_ovd = True if (i % 9 == 0 and status_val not in [TicketStatus.RESOLVED.value, TicketStatus.CLOSED.value]) else False

            ticket = Ticket(
                ticket_number=f"TKT-2026-{1000 + i}",
                title=f"{title_tpl} (#{i})",
                description=f"Detailed support request for {title_tpl}. Requester reports persistent issue affecting workflow. Step-by-step reproduction and logs attached.",
                category_id=categories_map[cat_name].id,
                priority=prio,
                status=status_val,
                requester_id=req_user.id,
                assigned_agent_id=assigned_agent.id if assigned_agent else None,
                department_id=depts_map[dept_code].id,
                first_response_due_at=resp_due,
                resolution_due_at=res_due,
                is_overdue=is_ovd,
                created_at=created_at,
                updated_at=created_at + timedelta(hours=1)
            )
            db.add(ticket)
            db.flush()

            # Public comment
            comment = TicketComment(
                ticket_id=ticket.id,
                author_id=assigned_agent.id if assigned_agent else mgr_it.id,
                content=f"Hello {req_user.full_name}, thank you for submitting this request. Our engineering team is currently investigating your ticket.",
                is_internal_note=False,
                created_at=created_at + timedelta(minutes=15)
            )
            db.add(comment)

            # Internal note (Agent only)
            if i % 2 == 0 and assigned_agent:
                internal_note = TicketComment(
                    ticket_id=ticket.id,
                    author_id=assigned_agent.id,
                    content=f"INTERNAL NOTE: Checked backend logs. Diagnostic trace indicates potential DNS cache delay. Escalating to Tier 2 if unresolved.",
                    is_internal_note=True,
                    created_at=created_at + timedelta(minutes=25)
                )
                db.add(internal_note)

            tickets_created += 1

        print("Seeding Announcements...")
        announcements = [
            Announcement(title="Scheduled System Maintenance: Active Directory & SSO Services", content="Please be advised that core authentication services will undergo scheduled maintenance on Saturday between 02:00 AM and 04:00 AM UTC. Single Sign-On may experience brief intermittent drops.", priority=AnnouncementPriority.IMPORTANT.value, target_audience="ALL", status=AnnouncementStatus.PUBLISHED.value, author_id=admin.id, published_at=now - timedelta(days=2)),
            Announcement(title="Updated IT Remote Work Security Policy 2026", content="All corporate laptops must update to Endpoint Protection Agent v5.4 before Sept 15. Compliance guidelines and download instructions are published in the Knowledge Base.", priority=AnnouncementPriority.NORMAL.value, target_audience="ALL", status=AnnouncementStatus.PUBLISHED.value, author_id=mgr_sec.id, published_at=now - timedelta(days=5)),
            Announcement(title="Upcoming Holiday IT Support Schedule", content="Over the upcoming bank holiday weekend, Tier 1 live chat support will operate on reduced hours (09:00 - 17:00). Critical Incident on-call engineers remain active 24/7.", priority=AnnouncementPriority.NORMAL.value, target_audience="ALL", status=AnnouncementStatus.PUBLISHED.value, author_id=mgr_it.id, published_at=now - timedelta(days=7))
        ]
        db.add_all(announcements)

        print("Seeding Knowledge Base Articles...")
        kb_articles = [
            KnowledgeBaseArticle(title="How to Connect to Corporate VPN via WireGuard Client", slug="connect-corporate-vpn-wireguard", category_id=categories_map["Network & VPN"].id, content="## Overview\nThis guide explains how to configure and connect to the secure corporate VPN.\n\n### Step 1: Install WireGuard\nDownload the official client for Windows or macOS.\n\n### Step 2: Import Configuration\nRequest your `.conf` key profile via TicketPro or download from the Security Portal.\n\n### Step 3: Connect\nClick Activate. Authenticate using MFA when prompted.", author_id=agents[1].id, status="PUBLISHED", view_count=342, helpful_count=48, unhelpful_count=2, tags="vpn,network,wireguard,remote"),
            KnowledgeBaseArticle(title="Troubleshooting macOS Wi-Fi Certificate Renewal Errors", slug="troubleshooting-macos-wifi-certificate", category_id=categories_map["Network & VPN"].id, content="If your Mac repeatedly prompts for Wi-Fi credentials or fails WPA2-Enterprise handshake, clear your Keychain certificate cache:\n1. Open Keychain Access\n2. Delete expired 'TicketPro-Corporate-WiFi' certs\n3. Reboot and reconnect.", author_id=agents[0].id, status="PUBLISHED", view_count=189, helpful_count=29, unhelpful_count=1, tags="wifi,macbook,certificate,keychain"),
            KnowledgeBaseArticle(title="Requesting AWS Staging Account IAM Roles & Access Keys", slug="requesting-aws-staging-iam-access", category_id=categories_map["Access & Permissions"].id, content="Engineering and DevOps team members can request developer access to AWS Staging environments by filing an Access Ticket in TicketPro. Approvals require Engineering Manager sign-off.", author_id=agents[2].id, status="PUBLISHED", view_count=521, helpful_count=84, unhelpful_count=3, tags="aws,iam,cloud,access,permissions")
        ]
        db.add_all(kb_articles)

        print("Seeding System Settings and Integrations...")
        settings = [
            SystemSetting(key="org_name", value="TicketPro Enterprise Corp", category="general"),
            SystemSetting(key="default_sla_hours", value="4", category="sla"),
            SystemSetting(key="auto_assign_enabled", value="true", category="routing")
        ]
        integrations = [
            Integration(name="Slack IT Operations Webhook", type="SLACK", config_json='{"webhook_url": "https://hooks.slack.com/services/mock", "channel": "#it-alerts"}', is_active=True),
            Integration(name="Microsoft Teams Incident Channel", type="TEAMS", config_json='{"webhook_url": "https://outlook.office.com/webhook/mock"}', is_active=False)
        ]
        db.add_all(settings + integrations)

        db.commit()
        print(f"Successfully seeded database with {tickets_created} tickets, 20+ users, departments, SLA policies, and KB articles!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
