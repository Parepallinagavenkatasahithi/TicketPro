from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.problem import Problem
from app.schemas.problem import ProblemCreate
from app.models.user import User

class ProblemManagementService:
    def __init__(self, db: Session):
        self.db = db

    def create_problem(self, prb_in: ProblemCreate, owner: User) -> Problem:
        count = self.db.query(Problem).count() + 1
        prb_num = f"PRB-2026-{1000 + count}"
        prb = Problem(
            problem_number=prb_num,
            title=prb_in.title,
            description=prb_in.description,
            root_cause=prb_in.root_cause,
            workaround=prb_in.workaround,
            status="INVESTIGATING",
            impact=prb_in.impact.upper(),
            owner_id=owner.id,
            department_id=prb_in.department_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.db.add(prb)
        self.db.commit()
        self.db.refresh(prb)
        return prb

    def list_problems(self) -> List[Problem]:
        return self.db.query(Problem).order_by(Problem.created_at.desc()).all()
