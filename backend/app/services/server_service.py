from sqlalchemy.ext.asyncio import AsyncSession
from app.models.server import Server
from app.repositories.server_repository import ServerRepository


class ServerService:

    def __init__(self):
        self.repository = ServerRepository()

    async def get_servers(
        self,
        session: AsyncSession,
    ) -> list[Server]:

        return await self.repository.get_all(session)

    async def get_server(
        self,
        session: AsyncSession,
        server_id: str,
    ) -> Server | None:

        return await self.repository.get_by_id(
            session,
            server_id,
        )