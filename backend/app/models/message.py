from sqlalchemy import String, ForeignKey, ForeignKeyConstraint, DateTime, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (ForeignKeyConstraint(['server_id', 'user_id'], ['members.server_id', 'members.user_id']),)
    message_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    server_id: Mapped[str] = mapped_column(String(100), ForeignKey("servers.server_id"), nullable=False, index=True)
    channel_id: Mapped[str] = mapped_column(String(100), ForeignKey("channels.channel_id"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False,index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    has_attachment: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_embed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    reaction_count: Mapped[int] = mapped_column(Integer, nullable=False)
    is_pinned: Mapped[bool] = mapped_column(Boolean, nullable=False)
    length: Mapped[int] = mapped_column(Integer, nullable=False)

    server = relationship("Server", back_populates="messages", overlaps="member,messages")
    channel = relationship("Channel", back_populates="messages")
    member = relationship("Member", back_populates="messages", overlaps="server,messages")