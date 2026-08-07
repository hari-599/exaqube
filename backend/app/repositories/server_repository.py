from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.server import Server


class ServerRepository:

    async def get_all(self, session: AsyncSession) -> list[Server]:
        result = await session.execute(
            select(Server).order_by(Server.server_name)
        )
        return result.scalars().all()

    async def get_by_id(
        self,
        session: AsyncSession,
        server_id: str,
    ) -> Server | None:

        result = await session.execute(
            select(Server).where(Server.server_id == server_id)
        )

        return result.scalar_one_or_none()