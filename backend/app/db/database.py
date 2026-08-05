from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncSession
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
session_local=async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)