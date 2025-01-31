from fastapi import FastAPI
from src.users.routers.user_router import router as user_router
from src.users.routers.auth_router import router as auth_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI backend!"}