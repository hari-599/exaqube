from fastapi import FastAPI
from app.core.config import settings
app= FastAPI(title="Discord Analytics Agent")
@app.get("/")
async def root():
    return {"database": settings.DATABASE_URL}