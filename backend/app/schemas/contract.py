from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ContractBase(BaseModel):
    contract_number: str
    title: str
    vendor_id: int
    contract_type: str = "SLA_SUPPORT"
    status: str = "ACTIVE"
    annual_cost: float = 0.0
    start_date: datetime
    end_date: datetime
    auto_renew: bool = False
    notice_period_days: int = 30
    document_url: Optional[str] = None
    notes: Optional[str] = None


class ContractCreate(ContractBase):
    pass


class ContractOut(ContractBase):
    id: int
    vendor_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
