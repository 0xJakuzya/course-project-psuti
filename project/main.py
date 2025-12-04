from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.api.v1 import api_router

app = FastAPI(title="Parking Management System")

app.include_router(api_router, prefix="/api/v1")
@app.get("/")
async def root():
    return {"message": "Parking API"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    return {"status": "healthy", "database": "connected"}