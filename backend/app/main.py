from fastapi import FastAPI
from app.core.config import settings
from app.api.routers.server import router as server_router
from app.api.routers.analytics import router as analytics_router

app= FastAPI(title="Discord Analytics Agent", version="1.0.0")
@app.get("/")
async def root():
    return {"database": settings.DATABASE_URL}

app.include_router(server_router)
app.include_router(analytics_router)