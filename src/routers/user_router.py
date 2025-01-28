from fastapi import APIRouter, HTTPException, Depends
from ..schemas.user_schema import UserCreate, UserUpdate, UserResponse
from ..services.user_service import UserService
from typing import List

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    return await user_service.create_user(user.username, user.email, user.password)

# @router.get("/{user_id}", response_model=UserResponse)
# async def get_user(user_id: int):
#    user = await user_service.get_user(user_id)
#    if not user:
#        raise HTTPException(status_code=404, detail="User not found")
#    return user

# @router.put("/{user_id}", response_model=UserResponse)
# async def update_user(user_id: int, user: UserUpdate):
#    updated_user = await user_service.update_user(user_id, user)
#    if not updated_user:
#        raise HTTPException(status_code=404, detail="User not found")
#    return updated_user

# @router.delete("/{user_id}")
# async def delete_user(user_id: int):
#    deleted = await user_service.delete_user(user_id)
#    if not deleted:
#        raise HTTPException(status_code=404, detail="User not found")
#    return {"message": "User deleted"}

# @router.post("/login")
# async def login(username: str, password: str):
#    token = await user_service.authenticate_user(username, password)
#    if not token:
#        raise HTTPException(status_code=401, detail="Invalid credentials")
#    return {"access_token": token}