from sqlalchemy import BigInteger, ForeignKey,Date,Integer
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.db.base import Base
from datetime import date as date_type

class ChannelDailyStats(Base):
    __tablename__ = "channel_daily_stats"
    channel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("channels.channel_id"), primary_key=True)
    server_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("servers.server_id"), primary_key=True)
    date: Mapped[date_type] = mapped_column(Date,primary_key=True)
    messages_count: Mapped[int] = mapped_column(Integer, nullable=False)
    active_users: Mapped[int] = mapped_column(Integer, nullable=False)

    channel = relationship("Channel", back_populates="channel_daily_stats")
    server = relationship("Server", back_populates="channel_daily_stats")