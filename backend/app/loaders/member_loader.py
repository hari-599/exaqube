from app.loaders.base_loader import BaseLoader
from app.models.member import Member
import pandas as pd


class MembersLoader(BaseLoader):

    @property
    def filename(self) -> str:
        return "members.csv"

    def load(self) -> None:
        df = self.read_csv()

        df["join_date"] = pd.to_datetime(df["join_date"])
        df["last_active"] = pd.to_datetime(df["last_active"])
        df = df.drop_duplicates(subset=["user_id", "server_id"], keep="last")

        for _, row in df.iterrows():
            member = Member(
                user_id=str(row["user_id"]),
                server_id=str(row["server_id"]),
                username=row["username"],
                display_name=row["display_name"],
                discriminator=str(row["discriminator"]),
                avatar_hash=row["avatar_hash"] if pd.notna(row["avatar_hash"]) else None,
                is_bot=bool(row["is_bot"]),
                join_date=row["join_date"],
                last_active=row["last_active"],
                roles=row["roles"],
                messages_sent=int(row["messages_sent"]),
                voice_minutes=int(row["voice_minutes"]),
                is_owner=bool(row["is_owner"]),
            )
            self.session.merge(member)

        try:
            self.session.commit()
            print(f"Loaded {len(df)} members.")
        except Exception:
            self.session.rollback()
            raise