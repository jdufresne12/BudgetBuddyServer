from pydantic import BaseModel, EmailStr
from ..schemas.user import UserData
from datetime import datetime
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    user_data: UserData
    access_token: str
    token_type: str = "bearer"
