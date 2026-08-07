from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.analytics import DashboardResponse,TopServerResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

service = AnalyticsService()


@router.get(
    "/dashboard",
    response_model=DashboardResponse,
)
async def get_dashboard(
    session: AsyncSession = Depends(get_db),
):
    return await service.get_dashboard(session)

@router.get(
    "/top_servers",
    response_model=list[TopServerResponse],
)
async def get_top_servers(
    session: AsyncSession = Depends(get_db),):
    return await service.get_top_servers(session)