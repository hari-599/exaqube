from app.loaders.base_loader import BaseLoader
from app.models.channel_daily_stats import ChannelDailyStats
import pandas as pd


class ChannelDailyStatsLoader(BaseLoader):

    @property
    def filename(self) -> str:
        return "channel_daily_stats.csv"

    def load(self) -> None:
        df = self.read_csv()

        df["date"] = pd.to_datetime(df["date"])
        df = df.drop_duplicates(subset=["channel_id", "server_id", "date"], keep="last")

        for _, row in df.iterrows():

            channel_stat = ChannelDailyStats(
                channel_id=str(row["channel_id"]),
                server_id=str(row["server_id"]),
                date=row["date"],
                messages_count=int(row["message_count"]),
                active_users=int(row["active_users"]),
            )
            self.session.merge(channel_stat)

        try:
            self.session.commit()
            print(f"Loaded {len(df)} channel daily stats.")
        except Exception:
            self.session.rollback()
            raise