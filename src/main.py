from fastapi import FastAPI
from src.routers.user_router import router as user_router
from src.routers.auth_router import router as auth_router
from src.routers.section_router import router as section_router
from src.routers.budget_router import router as budget_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
# app.include_router(section_router)
app.include_router(budget_router)   


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI backend!"}