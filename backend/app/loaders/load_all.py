from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.loaders.server_loader import ServersLoader
from app.loaders.channel_loader import ChannelsLoader
from app.loaders.member_loader import MembersLoader
from app.loaders.daily_stats_loader import DailyStatsLoader
from app.loaders.channels_daily_stat_loader import ChannelDailyStatsLoader
from app.loaders.message_loader import MessagesLoader


def main():

    data_dir = Path(__file__).resolve().parents[3] / "database" / "data"

    # create a synchronous DB session for bulk loading (avoid async session coroutines)
    sync_db_url = settings.DATABASE_URL.replace("+asyncpg", "")
    engine = create_engine(sync_db_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    loaders = [
        ServersLoader,
        ChannelsLoader,
        MembersLoader,
        DailyStatsLoader,
        ChannelDailyStatsLoader,
        MessagesLoader,
    ]

    try:

        for loader_class in loaders:

            print(f"\nLoading {loader_class.__name__}...")

            loader = loader_class(
                session=session,
                data_dir=data_dir,
            )

            loader.load()

        print("\nAll datasets loaded successfully!")

    except Exception as e:

        session.rollback()
        print(f"\nLoading failed: {e}")
        raise

    finally:

        session.close()


if __name__ == "__main__":
    main()