from fastapi import APIRouter, HTTPException, Request
from ..schemas.auth import LoginRequest, LoginResponse
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    try:
        user, access_token = await auth_service.login(login_data)
        if user and access_token:
            user_data = {
                'user_id': user.user_id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            return LoginResponse(
                user_data=user_data,
                access_token=access_token,
                token_type="bearer"
            )
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/logout")
async def logout(request: Request):
    try:
        token = request.headers.get("Authorization", "").split(" ")[1]
        await auth_service.logout(token)
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))