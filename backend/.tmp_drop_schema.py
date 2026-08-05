import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app.core.config import settings
from sqlalchemy import create_engine, text

engine = create_engine(settings.DATABASE_URL.replace('+asyncpg', ''))
with engine.connect() as conn:
    conn.execute(text('DROP TABLE IF EXISTS messages, channel_daily_stats, members, daily_stats, channels, servers, alembic_version CASCADE'))
    conn.commit()
print('Dropped old tables')
