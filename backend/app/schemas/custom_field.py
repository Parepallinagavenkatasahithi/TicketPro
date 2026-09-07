from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class CustomFieldBase(BaseModel):
    name: str
    field_key: str
    field_type: str = "TEXT"
    description: Optional[str] = None
    is_required: bool = False
    options_json: Optional[str] = None
    target_entity: str = "TICKET"
    is_active: bool = True
    display_order: int = 0


class CustomFieldCreate(CustomFieldBase):
    pass


class CustomFieldOut(CustomFieldBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomFieldValueBase(BaseModel):
    custom_field_id: int
    entity_id: int
    field_value: Optional[str] = None


class CustomFieldValueCreate(CustomFieldValueBase):
    pass


class CustomFieldValueOut(CustomFieldValueBase):
    id: int
    custom_field_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
