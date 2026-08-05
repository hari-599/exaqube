from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Channel(Base):
    __tablename__ = "channels"
    channel_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    server_id: Mapped[str] = mapped_column(ForeignKey("servers.server_id"), nullable=False)
    channel_name: Mapped[str] = mapped_column(String(255), nullable=False)
    channel_type: Mapped[str] = mapped_column(String(20), nullable=False)
    topic: Mapped[str] = mapped_column(String(255), nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    nsfw: Mapped[bool] = mapped_column(Boolean, nullable=False)
    rate_limit_per_user: Mapped[int] = mapped_column(Integer, nullable=False)

    server = relationship("Server", back_populates="channels")
    messages = relationship("Message", back_populates="channel")
    channel_daily_stats = relationship("ChannelDailyStats", back_populates="channel")


