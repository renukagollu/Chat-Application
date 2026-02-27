"""
MessageService.

Orchestrates sending and listing messages with authorization checks.
"""

from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import Session

from app.domain.errors import Forbidden, NotFound, ValidationError
from app.repositories.groups import GroupRepository
from app.repositories.users import UserRepository
from app.repositories.memberships import MembershipRepository
from app.repositories.messages import MessageRepository


class MessageService:
    """Business logic for messaging operations."""

    def __init__(
        self,
        groups: GroupRepository,
        users: UserRepository,
        memberships: MembershipRepository,
        messages: MessageRepository,
    ) -> None:
        """
        Initialize service with required repositories.

        Args:
            groups: Group repository.
            users: User repository.
            memberships: Membership repository.
            messages: Message repository.
        """
        self._groups = groups
        self._users = users
        self._memberships = memberships
        self._messages = messages

    def send_message(self, db: Session, group_id: int, username: str, content: str) -> dict:
        """
        Send a message to a group as a member.

        Args:
            db: SQLAlchemy session.
            group_id: Group ID.
            username: Username from request header.
            content: Message content.

        Raises:
            NotFound: If group does not exist.
            Forbidden: If user is not a member.
        """
        group = self._groups.get(db, group_id)
        if not group:
            raise NotFound("Group not found")

        user = self._users.get_or_create(db, username)
        if not self._memberships.is_member(db, user.id, group_id):
            raise Forbidden("Join the group before sending messages")

        msg = self._messages.create(db, group_id=group_id, user_id=user.id, content=content)
        return {"id": msg.id, "created_at": msg.created_at.isoformat()}

    def list_messages(self, db: Session, group_id: int, limit: int, after: str | None) -> list[dict]:
        """
        List messages from a group with simple pagination.

        Args:
            db: SQLAlchemy session.
            group_id: Group ID.
            limit: Max number of messages (validated/capped by route).
            after: Optional ISO timestamp string.

        Raises:
            NotFound: If group does not exist.
            ValidationError: If 'after' cannot be parsed.

        Returns:
            List of message payloads.
        """
        group = self._groups.get(db, group_id)
        if not group:
            raise NotFound("Group not found")

        after_dt: datetime | None = None
        if after:
            try:
                after_dt = datetime.fromisoformat(after)
            except ValueError as e:
                raise ValidationError("Invalid 'after' timestamp. Use ISO format.") from e

        # Prefer passing datetime into repository; here we keep repo simple.
        msgs = self._messages.list_by_group(db, group_id=group_id, limit=limit, after=after_dt.isoformat() if after_dt else None)

        # Joining usernames: for brevity, return without join.
        # In a real project you'd join users in repository.
        return [{"id": m.id, "content": m.content, "created_at": m.created_at.isoformat(), "user_id": m.user_id} for m in msgs]