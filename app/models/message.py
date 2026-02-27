"""
Message model.

Messages belong to a group and are authored by a user.
"""

from __future__ import annotations

from datetime import datetime
from sqlalchemy import ForeignKey, Text, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Message(Base):
    """Represents a message sent inside a group."""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


Index("idx_messages_group_created_at", Message.group_id, Message.created_at)