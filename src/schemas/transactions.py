from pydantic import BaseModel, EmailStr # type: ignore
from datetime import date, datetime
from typing import Optional

class Transaction(BaseModel): 
    transaction_id: int
    user_id: int
    item_id: int
    description: str
    amount: int
    type: str
    date: date

class CreateTransactionData(BaseModel): 
    user_id: int
    item_id: int
    description: str
    amount: int
    type: str
    date: date

class DeleteTransactionData(BaseModel):
    user_id: int
    transaction_id: int

class GetAllTransactionsData(BaseModel):
    user_id: int

class GetMonthsTransactionsData(BaseModel):
    user_id: int
    month: int
    year: int
