from fastapi import FastAPI
from utils.database import Database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await Database.connect()

@app.on_event("shutdown")
async def shutdown():
    if Database.pool:
        await Database.pool.close()