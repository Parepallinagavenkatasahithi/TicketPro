import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Created {path}")

def generate_backend_models():
    # Asset model
    asset_model = """
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False) # LAPTOP, DESKTOP, SERVER, MONITOR, PRINTER, NETWORK, OTHER
    model_number = Column(String(100), nullable=True)
    serial_number = Column(String(100), unique=True, nullable=True)
    status = Column(String(30), default="IN_USE") # IN_USE, IN_STOCK, UNDER_REPAIR, RETIRED, LOST
    
    assigned_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    location = Column(String(100), nullable=True)
    
    purchase_date = Column(DateTime(timezone=True), nullable=True)
    warranty_expiry_date = Column(DateTime(timezone=True), nullable=True)
    purchase_cost = Column(Float, nullable=True)
    vendor_name = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    assigned_user = relationship("User", foreign_keys=[assigned_to_user_id])
    department = relationship("Department", foreign_keys=[department_id])
"""
    create_file("backend/app/models/asset.py", asset_model)

    # Change Request model
    change_model = """
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ChangeRequest(Base):
    __tablename__ = "change_requests"

    id = Column(Integer, primary_key=True, index=True)
    change_number = Column(String(50), unique=True, nullable=False, index=True) # CHG-2026-1001
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    reason_for_change = Column(Text, nullable=False)
    impact_analysis = Column(Text, nullable=False)
    rollback_plan = Column(Text, nullable=False)
    
    category = Column(String(50), default="STANDARD") # STANDARD, NORMAL, EMERGENCY
    risk_level = Column(String(20), default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(30), default="DRAFT") # DRAFT, PENDING_APPROVAL, APPROVED, SCHEDULED, IN_PROGRESS, COMPLETED, REJECTED, CANCELLED
    
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_cab_lead_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    scheduled_start_at = Column(DateTime(timezone=True), nullable=True)
    scheduled_end_at = Column(DateTime(timezone=True), nullable=True)
    actual_start_at = Column(DateTime(timezone=True), nullable=True)
    actual_end_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    requester = relationship("User", foreign_keys=[requester_id])
    cab_lead = relationship("User", foreign_keys=[assigned_cab_lead_id])
"""
    create_file("backend/app/models/change_request.py", change_model)

    # Problem model
    problem_model = """
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    problem_number = Column(String(50), unique=True, nullable=False, index=True) # PRB-2026-1001
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=True)
    workaround = Column(Text, nullable=True)
    
    status = Column(String(30), default="INVESTIGATING") # LOGGED, INVESTIGATING, KNOWN_ERROR, RESOLVED, CLOSED
    impact = Column(String(20), default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = relationship("User", foreign_keys=[owner_id])
    department = relationship("Department", foreign_keys=[department_id])
"""
    create_file("backend/app/models/problem.py", problem_model)

    # Survey model
    survey_model = """
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    respondent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False) # 1 to 5 stars
    feedback_text = Column(Text, nullable=True)
    
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    ticket = relationship("Ticket")
    respondent = relationship("User", foreign_keys=[respondent_id])
    agent = relationship("User", foreign_keys=[agent_id])
"""
    create_file("backend/app/models/survey.py", survey_model)

    # Time tracking model
    time_model = """
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class TimeEntry(Base):
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hours_spent = Column(Float, nullable=False)
    activity_type = Column(String(50), default="RESEARCH") # RESEARCH, TROUBLESHOOTING, COMMUNICATION, REPAIR, DEPLOYMENT
    description = Column(Text, nullable=True)
    
    logged_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    ticket = relationship("Ticket")
    user = relationship("User")
"""
    create_file("backend/app/models/time_tracking.py", time_model)

if __name__ == "__main__":
    generate_backend_models()
