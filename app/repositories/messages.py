"""
MessageRepository.

Persistence operations for group messages.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:
    """Repository for message persistence operations."""

    def create(self, db: Session, group_id: int, user_id: int, content: str) -> Message:
        """
        Create and persist a message.

        Args:
            db: SQLAlchemy session.
            group_id: Group ID.
            user_id: Author user ID.
            content: Message content.

        Returns:
            The created message.
        """
        msg = Message(group_id=group_id, user_id=user_id, content=content)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg

    def list_by_group(self, db: Session, group_id: int, limit: int, after: str | None) -> list[Message]:
        """
        List messages for a given group.

        Args:
            db: SQLAlchemy session.
            group_id: Group ID.
            limit: Max number of messages (capped by API).
            after: Optional ISO timestamp string to filter messages strictly after it.

        Returns:
            List of messages ordered by created_at ascending.
        """
        stmt = select(Message).where(Message.group_id == group_id)

        if after:
            # Let service validate/parse; keep repository simple
            stmt = stmt.where(Message.created_at > after)  # type: ignore[operator]

        stmt = stmt.order_by(Message.created_at.asc()).limit(limit)
        return list(db.execute(stmt).scalars().all())