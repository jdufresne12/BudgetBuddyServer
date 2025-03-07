from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import List, Optional

from src.schemas.transactions import Transaction

class BudgetItem(BaseModel):
    item_id: int
    section_name: str
    user_id: int
    name: str
    amount: int
    type: str
    start_date: date
    end_date: Optional[date] = None

class BudgetItems(BaseModel):
    item_id: int
    section_name: str
    user_id: int
    name: str
    amount: int
    type: str
    start_date: date
    end_date: Optional[date] = None
    transactions: Optional[List[Transaction]] = []

class CreateBudgetItem(BaseModel):
    section_name: str
    user_id: int
    name: str
    amount: int
    type: str
    start_date: date
    end_date: Optional[date] = None

class CreateBudgetItemResponse(BaseModel):
    item_id: int
    section_name: str
    name: str
    amount: int
    type: str
    start_date: date
    end_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

class DeleteItemData(BaseModel):
    section_name: str
    user_id: int
    item_id: int

class GetBudgetData(BaseModel):
    user_id: int
    month: int
    year: int