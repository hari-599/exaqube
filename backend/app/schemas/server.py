from datetime import datetime
from pydantic import BaseModel,ConfigDict

class ServerResponse(BaseModel):
    server_id: str
    server_name: str
    owner_id: str
    creation_date: datetime
    region: str
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    system_channel_id: str | None

    model_config = ConfigDict(from_attributes=True)