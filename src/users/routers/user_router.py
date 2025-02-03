from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ..schemas.user import UserCreate
from ..schemas.user import UserResponse
from ..services.user_service import UserService
from ...utils.auth_token import verify_token

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()

@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate):
    try:
        user = await user_service.create_user(user_data)
        if user:
            return UserResponse(
                user_id=user.user_id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        raise HTTPException(status_code=400, detail="Could not create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, current_user: dict = Depends(verify_token)):
    try:
        user = await user_service.delete_user(user_id)
        if user:
            return UserResponse(
                user_id=user.user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        raise HTTPException(status_code=400, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[UserResponse])
async def get_all_users(current_user: dict = Depends(verify_token)):
    try:
        users = await user_service.get_all_users()
        if users:
            return [
                UserResponse(
                    user_id=user.user_id,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                ) for user in users
            ]
        raise HTTPException(status_code=404, detail="No users found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_users(user_id: int, current_user: dict = Depends(verify_token)):
    try:
        user = await user_service.get_user(user_id)
        if user:
            return UserResponse(
                user_id=user.user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        raise HTTPException(status_code=400, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    