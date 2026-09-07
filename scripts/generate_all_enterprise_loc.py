import os
import sys

def write_f(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

print("Generating Production Enterprise Modules...")

# 1. Asset CMDB Subpackage
write_f("backend/app/domain/asset_cmdb/models.py", '''
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class AssetInventoryItem(Base):
    __tablename__ = "asset_inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    asset_code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False, default="HARDWARE")
    model_name = Column(String(150), nullable=True)
    serial_number = Column(String(150), nullable=True)
    status = Column(String(50), default="IN_USE")
    purchase_cost = Column(Float, default=0.0)
    current_value = Column(Float, default=0.0)
    salvage_value = Column(Float, default=0.0)
    depreciation_method = Column(String(50), default="STRAIGHT_LINE")
    useful_life_years = Column(Integer, default=5)
    location_name = Column(String(150), nullable=True)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    vendor_name = Column(String(150), nullable=True)
    purchase_date = Column(DateTime(timezone=True), nullable=True)
    warranty_expiration = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    assigned_user = relationship("User", foreign_keys=[assigned_user_id])
    department = relationship("Department")
''')

write_f("backend/app/domain/asset_cmdb/depreciation.py", '''
from typing import Dict, Any

class DepreciationCalculator:
    """Calculates asset depreciation over time using straight-line or declining balance methods."""

    @staticmethod
    def calculate_straight_line(cost: float, salvage: float, useful_years: int, age_years: float) -> Dict[str, float]:
        if useful_years <= 0:
            return {"annual_depreciation": 0.0, "current_book_value": cost, "accumulated_depreciation": 0.0}
        
        annual_dep = max(cost - salvage, 0.0) / float(useful_years)
        accumulated = min(annual_dep * age_years, cost - salvage)
        book_value = max(cost - accumulated, salvage)

        return {
            "annual_depreciation": round(annual_dep, 2),
            "accumulated_depreciation": round(accumulated, 2),
            "current_book_value": round(book_value, 2)
        }

    @staticmethod
    def calculate_declining_balance(cost: float, salvage: float, useful_years: int, age_years: float, factor: float = 2.0) -> Dict[str, float]:
        if useful_years <= 0 or cost <= 0:
            return {"annual_depreciation": 0.0, "current_book_value": cost, "accumulated_depreciation": 0.0}

        rate = (1.0 / useful_years) * factor
        book_val = cost
        for _ in range(int(age_years)):
            dep = book_val * rate
            book_val = max(book_val - dep, salvage)

        return {
            "rate_percentage": round(rate * 100, 2),
            "current_book_value": round(book_val, 2),
            "accumulated_depreciation": round(cost - book_val, 2)
        }
''')

# 2. Change Request Subpackage
write_f("backend/app/domain/change_cab/risk_calculator.py", '''
from typing import Dict, Any, List

class CABRiskCalculator:
    """Calculates change request risk score based on infrastructure scope, rollbacks, and blackout windows."""

    RISK_MATRIX = {
        ("CRITICAL", "ENTERPRISE"): "EXTREME",
        ("HIGH", "ENTERPRISE"): "HIGH",
        ("HIGH", "DEPARTMENTAL"): "MEDIUM",
        ("LOW", "DEPARTMENTAL"): "LOW"
    }

    def evaluate_change_risk(
        self,
        category: str,
        impact_scope: str,
        has_rollback_plan: bool,
        is_during_blackout: bool,
        test_environment_verified: bool
    ) -> Dict[str, Any]:
        base_score = 10.0

        if category == "INFRASTRUCTURE":
            base_score += 25.0
        elif category == "DATABASE":
            base_score += 30.0
        elif category == "SECURITY_PATCH":
            base_score += 15.0

        if impact_scope == "ENTERPRISE":
            base_score += 35.0
        elif impact_scope == "BUSINESS_UNIT":
            base_score += 20.0

        if not has_rollback_plan:
            base_score += 20.0

        if is_during_blackout:
            base_score += 25.0

        if test_environment_verified:
            base_score -= 15.0

        score = min(max(base_score, 0.0), 100.0)

        if score >= 70.0:
            level = "CRITICAL"
            cab_votes_required = 3
        elif score >= 45.0:
            level = "HIGH"
            cab_votes_required = 2
        elif score >= 25.0:
            level = "MEDIUM"
            cab_votes_required = 1
        else:
            level = "LOW"
            cab_votes_required = 0

        return {
            "score": round(score, 2),
            "risk_level": level,
            "cab_approval_required": level in ["HIGH", "CRITICAL"],
            "cab_votes_required": cab_votes_required
        }
''')

# 3. Problem Management Subpackage
write_f("backend/app/domain/problem_mgmt/rca_engine.py", '''
from typing import List, Dict, Any

class RootCauseAnalysisEngine:
    """Manages 5-Whys root cause analysis, Ishikawa fishbone diagrams, and known error resolution."""

    @staticmethod
    def format_five_whys(whys: List[str]) -> Dict[str, Any]:
        steps = []
        for idx, text in enumerate(whys, 1):
            steps.append({"why_number": idx, "question": f"Why #{idx}", "answer": text})
        
        return {
            "total_whys": len(whys),
            "steps": steps,
            "root_cause_conclusion": whys[-1] if whys else "Root cause under investigation"
        }

    @staticmethod
    def evaluate_known_error_match(incident_description: str, known_errors: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        matches = []
        words = set(incident_description.lower().split())
        
        for ke in known_errors:
            ke_words = set(ke.get("keywords", "").lower().split())
            intersection = words.intersection(ke_words)
            if intersection:
                score = len(intersection) / float(len(ke_words) or 1)
                matches.append({
                    "known_error_id": ke.get("id"),
                    "title": ke.get("title"),
                    "workaround": ke.get("workaround"),
                    "confidence_score": round(min(score, 1.0), 2)
                })

        matches.sort(key=lambda x: x["confidence_score"], reverse=True)
        return matches
''')

print("Modules generated successfully!")
''')

print("Created generator script.")
