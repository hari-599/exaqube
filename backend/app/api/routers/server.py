from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.server import ServerResponse
from app.services.server_service import ServerService

router = APIRouter(prefix="/servers", tags=["servers"])
service=ServerService()

@router.get("/",response_model=list[ServerResponse])
async def get_servers(
    session: AsyncSession = Depends(get_db),
):
    return await service.get_servers(session)

@router.get("/{server_id}",response_model=ServerResponse)
async def get_server(
    server_id: str,
    session: AsyncSession = Depends(get_db),
):
    server = await service.get_server(session, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server
