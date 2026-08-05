from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Server(Base):
    __tablename__ = "servers"

    server_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    server_name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    creation_date: Mapped[str] = mapped_column(DateTime, nullable=False)
    region: Mapped[str] = mapped_column(String(255), nullable=False)
    verification_level: Mapped[str] = mapped_column(Integer, nullable=False)
    default_message_notifications: Mapped[str] = mapped_column(Integer, nullable=False)
    explicit_content_filter: Mapped[str] = mapped_column(Integer, nullable=False)
    system_channel_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    

    channels = relationship("Channel", back_populates="server")
    members = relationship("Member", back_populates="server")
    daily_stats = relationship("DailyStats", back_populates="server")
    messages = relationship("Message", back_populates="server", overlaps="member,messages")
    channel_daily_stats = relationship("ChannelDailyStats", back_populates="server")



