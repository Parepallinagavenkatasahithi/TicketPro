from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from app.models.contract import Contract
from app.schemas.contract import ContractCreate


class ContractService:
    def __init__(self, db: Session):
        self.db = db

    def list_contracts(self) -> List[Contract]:
        return self.db.query(Contract).order_by(Contract.end_date.asc()).all()

    def create_contract(self, c_in: ContractCreate) -> Contract:
        c = Contract(**c_in.model_dump())
        self.db.add(c)
        self.db.commit()
        self.db.refresh(c)
        return c
