from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime

class Member(Base):
    __tablename__ = "members"
    user_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    server_id: Mapped[str] = mapped_column(ForeignKey("servers.server_id"), primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)

    display_name: Mapped[str] = mapped_column(String(100), nullable=False)

    discriminator: Mapped[str] = mapped_column(String(4), nullable=False)

    avatar_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)

    is_bot: Mapped[bool] = mapped_column(Boolean, nullable=False)

    join_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    last_active: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    roles: Mapped[str | None] = mapped_column(String(255), nullable=True)

    messages_sent: Mapped[int] = mapped_column(Integer, nullable=False)

    voice_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    is_owner: Mapped[bool] = mapped_column(Boolean, nullable=False)

    server = relationship("Server", back_populates="members")
    messages = relationship("Message", back_populates="member", overlaps="server,messages")
