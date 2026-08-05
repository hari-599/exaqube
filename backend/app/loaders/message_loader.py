from app.loaders.base_loader import BaseLoader
from app.models.message import Message
import pandas as pd


class MessagesLoader(BaseLoader):

    @property
    def filename(self) -> str:
        return "messages_sample.csv"

    def load(self) -> None:
        df = self.read_csv()

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.drop_duplicates(subset=["message_id"], keep="last")

        for _, row in df.iterrows():

            message = Message(
                message_id=str(row["message_id"]),
                server_id=str(row["server_id"]),
                channel_id=str(row["channel_id"]),
                user_id=str(row["user_id"]),
                timestamp=row["timestamp"],
                content=row["content"],
                has_attachment=bool(row["has_attachment"]),
                has_embed=bool(row["has_embed"]),
                reaction_count=int(row["reaction_count"]),
                is_pinned=bool(row["is_pinned"]),
                length=int(row["length"]),
            )
            self.session.merge(message)

        try:
            self.session.commit()
            print(f"Loaded {len(df)} messages.")
        except Exception:
            self.session.rollback()
            raise