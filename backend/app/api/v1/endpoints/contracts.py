from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.contract import ContractOut, ContractCreate
from app.services.contract_service import ContractService
from app.security.rbac import get_current_user, require_permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[ContractOut])
def list_contracts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ContractService(db)
    contracts = service.list_contracts()
    results = []
    for c in contracts:
        results.append(ContractOut(
            id=c.id,
            contract_number=c.contract_number,
            title=c.title,
            vendor_id=c.vendor_id,
            vendor_name=c.vendor.name if c.vendor else None,
            contract_type=c.contract_type,
            status=c.status,
            annual_cost=c.annual_cost,
            start_date=c.start_date,
            end_date=c.end_date,
            auto_renew=c.auto_renew,
            notice_period_days=c.notice_period_days,
            document_url=c.document_url,
            notes=c.notes,
            created_at=c.created_at,
            updated_at=c.updated_at
        ))
    return results

@router.post("", response_model=ContractOut, status_code=status.HTTP_201_CREATED)
def create_contract(
    contract_in: ContractCreate,
    current_user: User = Depends(require_permission("settings.manage")),
    db: Session = Depends(get_db)
):
    service = ContractService(db)
    c = service.create_contract(contract_in)
    return ContractOut.model_validate(c)
