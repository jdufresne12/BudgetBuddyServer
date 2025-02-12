from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class CreateSectionData(BaseModel):
    user_id: int
    name: str
    start_date: date
    end_date: Optional[date] = None

class CreateSectionResponse(BaseModel):
    section_id: int
    name: str
    start_date: date
    end_date: Optional[date] = None

class GetMonthsSectionsData(BaseModel): 
    user_id: int
    month: int
    year: int

class DeleteSectionData(BaseModel): 
    user_id: int
    section_id: int
