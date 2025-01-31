from fastapi import APIRouter, HTTPException
from ..schemas.auth import LoginRequest, LoginResponse
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    try:
        user, access_token = await auth_service.login(login_data)
        if user and access_token:
            return LoginResponse(
                user_id=user.user_id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                access_token=access_token,
                token_type="bearer"
            )
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))