from sqlalchemy import String, ForeignKey, Date, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import date as date_type

class DailyStats(Base):
    __tablename__ = "daily_stats"
    server_id: Mapped[str] = mapped_column(String(100), ForeignKey("servers.server_id"), primary_key=True)
    date: Mapped[date_type] = mapped_column(Date, primary_key=True)
    total_messages: Mapped[int] = mapped_column(Integer, nullable=False)
    new_members: Mapped[int] = mapped_column(Integer, nullable=False)
    total_members: Mapped[int] = mapped_column(Integer, nullable=False)
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    is_weekend: Mapped[bool] = mapped_column(Boolean, nullable=False)
    active_members: Mapped[int] = mapped_column(Integer, nullable=False)
    server = relationship("Server", back_populates="daily_stats")