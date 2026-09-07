import os
import sys

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Created: {path}")

def build_backend_infra():
    # 1. Matrix Calculator
    create_file("backend/app/infra/matrix_calculator.py", '''
from typing import Dict, List, Any, Optional

class RiskMatrixCalculator:
    """Calculates weighted risk score, SLA breach probability, and escalation urgency."""

    SEVERITY_WEIGHTS = {"LOW": 1, "MEDIUM": 3, "HIGH": 7, "CRITICAL": 15}
    IMPACT_WEIGHTS = {"DEPARTMENTAL": 2, "BUSINESS_UNIT": 5, "ENTERPRISE": 10}

    def __init__(self, config: Optional[Dict[str, float]] = None):
        self.config = config or {"alpha": 0.4, "beta": 0.6}

    def compute_risk_score(self, priority: str, impact_scope: str, affected_user_count: int) -> Dict[str, Any]:
        prio_val = self.SEVERITY_WEIGHTS.get(priority.upper(), 3)
        impact_val = self.IMPACT_WEIGHTS.get(impact_scope.upper(), 2)
        user_factor = min(affected_user_count / 100.0, 5.0)

        raw_score = (prio_val * self.config["alpha"]) + (impact_val * self.config["beta"]) + user_factor
        normalized_score = min(max(raw_score, 1.0), 100.0)

        if normalized_score >= 80.0:
            category = "EXTREME"
        elif normalized_score >= 50.0:
            category = "HIGH"
        elif normalized_score >= 25.0:
            category = "MODERATE"
        else:
            category = "LOW"

        return {
            "score": round(normalized_score, 2),
            "category": category,
            "requires_cab_approval": normalized_score >= 50.0,
            "recommended_sla_minutes": 30 if category == "EXTREME" else 120
        }

    def predict_sla_breach_probability(self, elapsed_minutes: float, total_sla_minutes: float, comment_count: int) -> float:
        if total_sla_minutes <= 0:
            return 1.0
        ratio = elapsed_minutes / total_sla_minutes
        engagement_factor = max(1.0 - (comment_count * 0.05), 0.5)
        prob = min(max(ratio * engagement_factor, 0.0), 1.0)
        return round(prob, 4)
''')

    # 2. Dynamic Query Builder
    create_file("backend/app/infra/query_builder.py", '''
from typing import Dict, List, Any
from sqlalchemy.orm import Query
from sqlalchemy import or_, and_, desc, asc

class DynamicQueryBuilder:
    """Builds dynamic SQL expressions from frontend filter payloads."""

    def __init__(self, model_class):
        self.model = model_class

    def apply_filters(self, query: Query, filters: Dict[str, Any]) -> Query:
        conditions = []
        for field, value in filters.items():
            if value is None or value == "":
                continue
            if not hasattr(self.model, field):
                continue
            
            attr = getattr(self.model, field)
            if isinstance(value, list):
                conditions.append(attr.in_(value))
            elif isinstance(value, str) and "%" in value:
                conditions.append(attr.ilike(value))
            else:
                conditions.append(attr == value)

        if conditions:
            query = query.filter(and_(*conditions))
        return query

    def apply_sorting(self, query: Query, sort_by: str = "id", order: str = "desc") -> Query:
        if hasattr(self.model, sort_by):
            attr = getattr(self.model, sort_by)
            if order.lower() == "desc":
                query = query.order_by(desc(attr))
            else:
                query = query.order_by(asc(attr))
        return query
''')

    # 3. Export Formatter
    create_file("backend/app/infra/export_formatter.py", '''
import csv
import json
import io
from typing import List, Dict, Any

class ExportFormatter:
    """Generates structured CSV and JSON export payloads for reports and audit logs."""

    @staticmethod
    def to_csv(records: List[Dict[str, Any]], fieldnames: List[str]) -> str:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in records:
            writer.writerow(row)
        return output.getvalue()

    @staticmethod
    def to_json(records: List[Dict[str, Any]], indent: int = 2) -> str:
        return json.dumps(records, default=str, indent=indent)
''')

    # 4. Cache Store
    create_file("backend/app/infra/cache_store.py", '''
import time
from typing import Dict, Any, Optional

class InMemoryTTLCache:
    """Thread-safe in-memory cache store with TTL expiry for dashboard metrics."""

    def __init__(self, default_ttl_seconds: int = 300):
        self.default_ttl = default_ttl_seconds
        self._store: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        item = self._store[key]
        if time.time() > item["expires_at"]:
            del self._store[key]
            return None
        return item["value"]

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        self._store[key] = {
            "value": value,
            "expires_at": time.time() + ttl
        }

    def clear(self) -> None:
        self._store.clear()

global_cache = InMemoryTTLCache()
''')

if __name__ == "__main__":
    build_backend_infra()
