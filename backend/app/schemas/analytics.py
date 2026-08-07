from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_servers: int
    total_members: int
    total_messages: int
    active_members: int

class TopServerResponse(BaseModel):
    server_id: str
    server_name: str
    total_messages: int