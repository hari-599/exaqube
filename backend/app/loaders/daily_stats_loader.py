from app.loaders.base_loader import BaseLoader
from app.models.daily_stats import DailyStats
import pandas as pd


class DailyStatsLoader(BaseLoader):

    @property
    def filename(self) -> str:
        return "daily_stats.csv"

    def load(self) -> None:
        df = self.read_csv()

        df["date"] = pd.to_datetime(df["date"])
        df = df.drop_duplicates(subset=["server_id", "date"], keep="last")

        for _, row in df.iterrows():
            stat = DailyStats(
                server_id=str(row["server_id"]),
                date=row["date"],
                total_messages=int(row["total_messages"]),
                new_members=int(row["new_members"]),
                total_members=int(row["total_members"]),
                day_of_week=int(row["day_of_week"]),
                is_weekend=bool(row["is_weekend"]),
                active_members=int(row["active_members"]),
            )
            self.session.merge(stat)

        try:
            self.session.commit()
            print(f"Loaded {len(df)} daily stats.")
        except Exception:
            self.session.rollback()
            raise