from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from app.models.custom_field import CustomField, CustomFieldValue
from app.schemas.custom_field import CustomFieldCreate, CustomFieldValueCreate


class CustomFieldService:
    def __init__(self, db: Session):
        self.db = db

    def list_custom_fields(self, target_entity: str = "TICKET") -> List[CustomField]:
        return self.db.query(CustomField).filter(CustomField.target_entity == target_entity, CustomField.is_active == True).all()

    def create_custom_field(self, cf_in: CustomFieldCreate) -> CustomField:
        cf = CustomField(**cf_in.model_dump())
        self.db.add(cf)
        self.db.commit()
        self.db.refresh(cf)
        return cf

    def set_field_value(self, val_in: CustomFieldValueCreate) -> CustomFieldValue:
        val = CustomFieldValue(**val_in.model_dump())
        self.db.add(val)
        self.db.commit()
        self.db.refresh(val)
        return val
