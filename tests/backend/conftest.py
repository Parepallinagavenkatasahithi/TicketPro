import pytest
import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'backend')))

from app.core.database import Base, get_db
from app.main import app
from app.core.security import get_password_hash
from app.models.user import User, Role
from app.models.department import Department
from app.models.ticket import TicketCategory, Ticket, TicketStatus, TicketPriority
from app.models.sla import SLAPolicy

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_ticketpro.db"

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Roles
    admin_role = Role(name="ADMIN", description="System Admin")
    mgr_role = Role(name="MANAGER", description="Department Manager")
    agent_role = Role(name="AGENT", description="Support Agent")
    emp_role = Role(name="EMPLOYEE", description="Employee")
    db.add_all([admin_role, mgr_role, agent_role, emp_role])
    db.flush()

    # Department
    it_dept = Department(name="Information Technology", code="IT", description="IT Dept")
    db.add(it_dept)
    db.flush()

    # SLA Policy
    sla_med = SLAPolicy(name="Medium SLA", priority="MEDIUM", max_first_response_minutes=120, max_resolution_minutes=480, is_default=True)
    db.add(sla_med)
    db.flush()

    # Ticket Category
    cat_hw = TicketCategory(name="Hardware", description="Hardware issues", default_priority="MEDIUM", default_department_id=it_dept.id)
    db.add(cat_hw)
    db.flush()

    # Users
    pwd_hash = get_password_hash("TestPassword123!")
    admin_user = User(employee_id="EMP-9000", email="admin.test@ticketpro.internal", hashed_password=pwd_hash, full_name="Test Admin", role_id=admin_role.id, role_name="ADMIN", department_id=it_dept.id)
    agent_user = User(employee_id="EMP-9001", email="agent.test@ticketpro.internal", hashed_password=pwd_hash, full_name="Test Agent", role_id=agent_role.id, role_name="AGENT", department_id=it_dept.id)
    emp_user = User(employee_id="EMP-9002", email="employee.test@ticketpro.internal", hashed_password=pwd_hash, full_name="Test Employee", role_id=emp_role.id, role_name="EMPLOYEE", department_id=it_dept.id)
    db.add_all([admin_user, agent_user, emp_user])

    db.commit()
    db.close()

    yield

    try:
        if os.path.exists("./test_ticketpro.db"):
            os.remove("./test_ticketpro.db")
    except Exception:
        pass


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db):
    def _override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
