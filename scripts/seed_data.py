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
from app.models.asset import Asset
from app.models.change_request import ChangeRequest
from app.models.problem import Problem
from app.models.survey import SurveyResponse
from app.models.time_tracking import TimeEntry
from app.models.vendor import Vendor, SoftwareLicense
from app.models.contract import Contract
from app.models.on_call import OnCallRotation, OnCallShift
from app.models.service_catalog import ServiceCatalogCategory, ServiceCatalogItem
from app.models.custom_field import CustomField
from app.models.email_template import EmailTemplate

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
            SLAPolicy(name="Critical Priority SLA", priority="CRITICAL", max_first_response_minutes=15, max_resolution_minutes=120, warning_threshold_percent=75, is_default=False),
            SLAPolicy(name="High Priority SLA", priority="HIGH", max_first_response_minutes=60, max_resolution_minutes=240, warning_threshold_percent=80, is_default=False),
            SLAPolicy(name="Medium Priority SLA", priority="MEDIUM", max_first_response_minutes=120, max_resolution_minutes=480, warning_threshold_percent=80, is_default=True),
            SLAPolicy(name="Low Priority SLA", priority="LOW", max_first_response_minutes=240, max_resolution_minutes=1440, warning_threshold_percent=85, is_default=False)
        ]
        db.add_all(sla_policies)
        db.flush()

        print("Seeding Ticket Categories...")
        categories_data = [
            ("Hardware & Laptops", "Laptops, monitors, workstations, peripherals, and replacement parts", "MEDIUM", "IT"),
            ("Software & SaaS", "App crashes, license activation, installation, and browser issues", "MEDIUM", "IT"),
            ("Network & VPN", "Wi-Fi connectivity, WireGuard VPN, firewall rules, and DNS resolution", "HIGH", "IT"),
            ("Access & Permissions", "Active Directory, IAM roles, SSO login, and password resets", "HIGH", "SEC"),
            ("Email & Collaboration", "Exchange email, Outlook, Slack channels, and MS Teams", "LOW", "IT"),
            ("Facilities & Workspace", "Desk assignments, HVAC temperature, badge keycards, and physical repairs", "LOW", "FAC"),
            ("HR & Payroll Support", "Benefits, direct deposit, employment verification, and leave requests", "LOW", "HR"),
            ("Financial & Expenses", "Reimbursements, purchase orders, vendor billing, and corporate card", "MEDIUM", "FIN")
        ]
        categories_map = {}
        for name, desc, prio, dept_code in categories_data:
            cat = TicketCategory(name=name, description=desc, default_priority=prio, default_department_id=depts_map[dept_code].id)
            db.add(cat)
            db.flush()
            categories_map[name] = cat

        print("Seeding Users and Employees...")
        hashed_password = get_password_hash("Password123!")

        # System Admin
        admin = User(employee_id="EMP-1000", email="admin@ticketpro.internal", hashed_password=hashed_password, full_name="Sarah Connor", job_title="VP of IT Operations", role_id=roles_map["ADMIN"].id, role_name="ADMIN", department_id=depts_map["IT"].id, is_active=True, is_verified=True)
        db.add(admin)

        # Department Managers
        mgr_it = User(employee_id="EMP-1001", email="it.manager@ticketpro.internal", hashed_password=hashed_password, full_name="Marcus Vance", job_title="IT Operations Manager", role_id=roles_map["MANAGER"].id, role_name="MANAGER", department_id=depts_map["IT"].id, is_active=True, is_verified=True)
        mgr_sec = User(employee_id="EMP-1002", email="sec.manager@ticketpro.internal", hashed_password=hashed_password, full_name="Elena Rostova", job_title="CISO & InfoSec Lead", role_id=roles_map["MANAGER"].id, role_name="MANAGER", department_id=depts_map["SEC"].id, is_active=True, is_verified=True)
        mgr_hr = User(employee_id="EMP-1003", email="hr.manager@ticketpro.internal", hashed_password=hashed_password, full_name="Patricia Arquette", job_title="HR Operations Director", role_id=roles_map["MANAGER"].id, role_name="MANAGER", department_id=depts_map["HR"].id, is_active=True, is_verified=True)
        db.add_all([mgr_it, mgr_sec, mgr_hr])

        # Support Agents
        agent_names = [
            ("EMP-2001", "Alex Rivera", "Senior Systems Engineer", "agent.alex@ticketpro.internal", "IT"),
            ("EMP-2002", "David Kim", "Network Operations Lead", "agent.david@ticketpro.internal", "IT"),
            ("EMP-2003", "Rachel Chen", "Cybersecurity Specialist", "agent.rachel@ticketpro.internal", "SEC"),
            ("EMP-2004", "James Thorne", "Helpdesk Specialist Tier 2", "agent.james@ticketpro.internal", "IT"),
            ("EMP-2005", "Sophia Martinez", "Facilities Administrator", "agent.sophia@ticketpro.internal", "FAC")
        ]
        agents = []
        for emp_id, name, title, email, dept_code in agent_names:
            u = User(employee_id=emp_id, email=email, hashed_password=hashed_password, full_name=name, job_title=title, role_id=roles_map["AGENT"].id, role_name="AGENT", department_id=depts_map[dept_code].id, is_active=True, is_verified=True)
            db.add(u)
            agents.append(u)

        # Standard Employees
        emp_names = [
            ("EMP-3001", "Brian O'Conner", "Senior Software Engineer", "brian.oconner@ticketpro.internal", "ENG"),
            ("EMP-3002", "Mia Toretto", "Financial Analyst", "mia.toretto@ticketpro.internal", "FIN"),
            ("EMP-3003", "Dominic Toretto", "Logistics Director", "dom.toretto@ticketpro.internal", "OPS"),
            ("EMP-3004", "Letty Ortiz", "DevOps Engineer", "letty.ortiz@ticketpro.internal", "ENG"),
            ("EMP-3005", "Han Lue", "Data Architect", "han.lue@ticketpro.internal", "ENG"),
            ("EMP-3006", "Gisele Yashar", "Talent Acquisition Specialist", "gisele.yashar@ticketpro.internal", "HR"),
            ("EMP-3007", "Roman Pearce", "Accounts Payable Lead", "roman.pearce@ticketpro.internal", "FIN"),
            ("EMP-3008", "Tej Parker", "Principal Cloud Architect", "tej.parker@ticketpro.internal", "ENG")
        ]
        employees = []
        for emp_id, name, title, email, dept_code in emp_names:
            u = User(employee_id=emp_id, email=email, hashed_password=hashed_password, full_name=name, job_title=title, role_id=roles_map["EMPLOYEE"].id, role_name="EMPLOYEE", department_id=depts_map[dept_code].id, is_active=True, is_verified=True)
            db.add(u)
            employees.append(u)

        db.flush()

        print("Seeding Vendors and Licenses...")
        v1 = Vendor(name="Apple Enterprise Direct", code="APPLE", contact_name="Tim Cook", contact_email="enterprise@apple.com", rating=4.9)
        v2 = Vendor(name="Datadog APM & Monitoring", code="DATADOG", contact_name="Jason Miller", contact_email="support@datadog.com", rating=4.8)
        db.add_all([v1, v2])
        db.flush()

        lic1 = SoftwareLicense(vendor_id=v2.id, software_name="Datadog Infrastructure Monitoring", license_type="PER_USER", total_seats=100, allocated_seats=45, cost_per_seat=120.0)
        db.add(lic1)

        print("Seeding Assets...")
        ast1 = Asset(asset_tag="AST-2026-001", name="MacBook Pro 16 M3 Max", category="HARDWARE", model_number="MBP-16", serial_number="C02XG011MD6R", status="IN_USE", purchase_cost=3499.0, assigned_to_user_id=admin.id, department_id=depts_map["IT"].id)
        ast2 = Asset(asset_tag="AST-2026-002", name="Dell UltraSharp 32 4K Monitor", category="HARDWARE", model_number="U3223QE", serial_number="CN098123456", status="IN_STOCK", purchase_cost=899.0, department_id=depts_map["IT"].id)
        db.add_all([ast1, ast2])

        print("Seeding Service Catalog...")
        cat1 = ServiceCatalogCategory(name="Hardware Requests", description="Request new workstations, monitors, and devices", icon_name="Laptop")
        db.add(cat1)
        db.flush()

        item1 = ServiceCatalogItem(category_id=cat1.id, name="Developer Workstation Pro", short_description="Apple MacBook Pro 16 or Dell XPS 15", estimated_fulfillment_hours=48.0, requires_approval=True, cost=2500.0)
        db.add(item1)

        print("Seeding Change Requests & Problems...")
        chg1 = ChangeRequest(change_number="CHG-2026-1001", title="Upgrade Core Switch Stack Firmware", description="Apply emergency security patch CVE-2026-8910", reason_for_change="Fix core switch buffer leak", impact_analysis="15 min brief network drop", rollback_plan="Revert to v3.1 image", category="INFRASTRUCTURE", risk_level="MEDIUM", status="APPROVED", requester_id=admin.id)
        prb1 = Problem(problem_number="PRB-2026-1001", title="Intermittent Database Connection Pool Timeout", description="Spikes in active DB connections exhaust pool under heavy loads", status="INVESTIGATING", impact="HIGH", owner_id=admin.id)
        db.add_all([chg1, prb1])

        print("Seeding Announcements...")
        now = datetime.now(timezone.utc)
        announcements = [
            Announcement(title="Scheduled System Maintenance: Active Directory & SSO Services", content="Please be advised that core authentication services will undergo scheduled maintenance on Saturday between 02:00 AM and 04:00 AM UTC. Single Sign-On may experience brief intermittent drops.", priority=AnnouncementPriority.IMPORTANT.value, target_audience="ALL", status=AnnouncementStatus.PUBLISHED.value, author_id=admin.id, published_at=now - timedelta(days=2)),
            Announcement(title="Updated IT Remote Work Security Policy 2026", content="All corporate laptops must update to Endpoint Protection Agent v5.4 before Sept 15. Compliance guidelines and download instructions are published in the Knowledge Base.", priority=AnnouncementPriority.NORMAL.value, target_audience="ALL", status=AnnouncementStatus.PUBLISHED.value, author_id=mgr_sec.id, published_at=now - timedelta(days=5))
        ]
        db.add_all(announcements)

        print("Seeding System Settings...")
        settings = [
            SystemSetting(key="org_name", value="TicketPro Enterprise Corp", category="general"),
            SystemSetting(key="default_sla_hours", value="4", category="sla"),
            SystemSetting(key="auto_assign_enabled", value="true", category="routing")
        ]
        db.add_all(settings)

        db.commit()
        print("Successfully seeded database with Users, ITIL Assets, Change Requests, Problems, Service Catalog, and System Settings!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
