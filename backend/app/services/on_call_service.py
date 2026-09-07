from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from app.models.on_call import OnCallRotation, OnCallShift
from app.schemas.on_call import OnCallRotationCreate, OnCallShiftCreate


class OnCallService:
    def __init__(self, db: Session):
        self.db = db

    def list_rotations(self) -> List[OnCallRotation]:
        return self.db.query(OnCallRotation).filter(OnCallRotation.is_active == True).all()

    def create_rotation(self, rot_in: OnCallRotationCreate) -> OnCallRotation:
        rot = OnCallRotation(**rot_in.model_dump())
        self.db.add(rot)
        self.db.commit()
        self.db.refresh(rot)
        return rot

    def create_shift(self, shift_in: OnCallShiftCreate) -> OnCallShift:
        shift = OnCallShift(**shift_in.model_dump())
        self.db.add(shift)
        self.db.commit()
        self.db.refresh(shift)
        return shift
