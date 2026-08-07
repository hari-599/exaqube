from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.analytics_repository import AnalyticsRepository
from app.schemas.analytics import DashboardResponse,TopServerResponse


class AnalyticsService:
    def __init__(self):
        self.repository = AnalyticsRepository()

    async def get_dashboard(
        self,
        session: AsyncSession,
    ) -> DashboardResponse:

        total_servers = await self.repository.get_total_servers(session)
        total_members = await self.repository.get_total_members(session)
        total_messages = await self.repository.get_total_messages(session)
        active_members = await self.repository.get_active_members(session)

        return DashboardResponse(
            total_servers=total_servers,
            total_members=total_members,
            total_messages=total_messages,
            active_members=active_members,
        )

    async def get_top_servers(self,session,limit: int = 5) -> list[TopServerResponse]:
        rows=await self.repository.get_top_servers(session,limit)
        return [TopServerResponse(server_id=row.server_id,server_name=row.server_name,total_messages=row.total_messages) for row in rows]