from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class BudgetItem(BaseModel):
    item_id: int
    section_id: int
    user_id: int
    name: str
    amount: int
    type: str
    start_date: date
    end_date: Optional[date] = None

class CreateBudgetItem(BaseModel):
    section_id: int
    user_id: int
    name: str
    amount: int
    type: str
    start_date: date
    end_date: Optional[date] = None

class CreateBudgetItemResponse(BaseModel):
    item_id: int
    section_id: int
    name: str
    amount: int
    type: str
    start_date: date
    end_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

class DeleteItemData(BaseModel):
    section_id: int
    user_id: int
    item_id: int

class GetSectionsItemsData(BaseModel):
    section_id: int
    user_id: int