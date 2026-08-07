from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.server import Server
from app.models.message import Message
from app.models.member import Member
from app.models.daily_stats import DailyStats

class AnalyticsRepository:

    async def get_total_servers(self, session: AsyncSession) -> int:
        result = await session.execute(
            select(func.count(Server.server_id))
        )
        return result.scalar_one()

    async def get_total_members(self, session: AsyncSession) -> int:
        result = await session.execute(
            select(func.count(Member.user_id))
        )
        return result.scalar_one()

    async def get_total_messages(self, session: AsyncSession) -> int:
        result = await session.execute(
            select(func.count(Message.message_id))
        )
        return result.scalar_one()

    async def get_active_members(self, session: AsyncSession) -> int:
        result = await session.execute(
            select(func.sum(DailyStats.active_members))
        )
        return result.scalar_one() or 0

    async def get_top_servers(self, session: AsyncSession,
                                  limit: int = 5,
                                  ):
        result = await session.execute(
            select(
                Server.server_id,
                Server.server_name,
                func.count(Message.message_id).label("total_messages"),
            )
            .join(
                Message,
                Server.server_id == Message.server_id,
            )
            .group_by(
                Server.server_id,
                Server.server_name,
            )
            .order_by(
                func.count(Message.message_id).desc()
            )
            .limit(limit)
        )

        return result.all()