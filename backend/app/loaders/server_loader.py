from app.loaders.base_loader import BaseLoader
from app.models.server import Server
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

class ServersLoader(BaseLoader):

    @property
    def filename(self) -> str:
        return "servers.csv"

    def load(self) -> None:
        df = self.read_csv()

        required_columns = {
            "server_id",
            "server_name",
            "owner_id",
            "creation_date",
            "region",
            "verification_level",
            "default_message_notifications",
            "explicit_content_filter",
            "system_channel_id",
        }

        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(f"Missing columns: {missing}")

        servers = []

        for _, row in df.iterrows():
            server = Server(
                server_id=str(row["server_id"]),
                server_name=row["server_name"],
                owner_id=str(row["owner_id"]),
                creation_date=pd.to_datetime(row["creation_date"]),
                region=row["region"],
                verification_level=_parse_int_field(row["verification_level"]),
                default_message_notifications=_parse_int_field(row["default_message_notifications"]),
                explicit_content_filter=_parse_int_field(row["explicit_content_filter"]),
                system_channel_id=str(row["system_channel_id"]) if pd.notna(row.get("system_channel_id")) else None )

            servers.append(server)

        try:
            for server in servers:
                self.session.merge(server)
            self.session.commit()
            print(f"Loaded {len(servers)} servers.")
        except Exception as e:
            self.session.rollback()
            print(f"Failed to load servers: {e}")
            raise