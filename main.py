from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from project.app.core.db import get_db

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Parking API"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    return {"status": "healthy", "database": "connected"}