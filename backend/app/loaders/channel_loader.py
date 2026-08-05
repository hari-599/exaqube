from app.loaders.base_loader import BaseLoader
from app.models.channel import Channel
import pandas as pd
import re


def _parse_int_field(value):
    if pd.isna(value):
        return None
    try:
        return int(value)
    except Exception:
        s = str(value)
        m = re.search(r"\d+", s)
        if m:
            return int(m.group())
        raise


class ChannelsLoader(BaseLoader):

    @property
    def filename(self) -> str:
        return "channels.csv"

    def load(self) -> None:
        df = self.read_csv()

        required_columns = {
            "channel_id",
            "server_id",
            "channel_name",
            "channel_type",
            "topic",
            "position",
        }

        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        channels = []

        for _, row in df.iterrows():
            channels.append(
                Channel(
                    channel_id=str(row["channel_id"]),
                    server_id=str(row["server_id"]),
                    channel_name=row["channel_name"],
                    channel_type=row["channel_type"],
                    topic=row["topic"] if row["topic"] == row["topic"] else None,
                    position=_parse_int_field(row["position"]),
                    nsfw=bool(row["nsfw"]) if "nsfw" in row else False,
                    rate_limit_per_user=_parse_int_field(row.get("rate_limit_per_user"))
                )
            )

        try:
            for ch in channels:
                self.session.merge(ch)
            self.session.commit()
            print(f"Loaded {len(channels)} channels.")
        except Exception:
            self.session.rollback()
            raise