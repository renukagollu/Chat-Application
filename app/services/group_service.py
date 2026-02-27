"""
GroupService.

Orchestrates group creation and membership behavior.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.errors import NotFound
from app.repositories.groups import GroupRepository
from app.repositories.users import UserRepository
from app.repositories.memberships import MembershipRepository


class GroupService:
    """Business logic for group operations."""

    def __init__(
        self,
        groups: GroupRepository,
        users: UserRepository,
        memberships: MembershipRepository,
    ) -> None:
        """
        Initialize service with required repositories.

        Args:
            groups: Group repository.
            users: User repository.
            memberships: Membership repository.
        """
        self._groups = groups
        self._users = users
        self._memberships = memberships

    def create_group(self, db: Session, name: str) -> dict:
        """
        Create a new group.

        Args:
            db: SQLAlchemy session.
            name: Group name.

        Returns:
            Dict representation of created group (id, name).
        """
        group = self._groups.create(db, name)
        return {"id": group.id, "name": group.name}

    def list_groups(self, db: Session) -> list[dict]:
        """
        List all groups.

        Args:
            db: SQLAlchemy session.

        Returns:
            List of dict representations of groups.
        """
        return [{"id": g.id, "name": g.name, "created_at": g.created_at.isoformat()} for g in self._groups.list(db)]

    def join_group(self, db: Session, group_id: int, username: str) -> dict:
        """
        Join a group as the given user (idempotent).

        Args:
            db: SQLAlchemy session.
            group_id: Group ID.
            username: Username from request header.

        Raises:
            NotFound: If group does not exist.

        Returns:
            Confirmation payload.
        """
        group = self._groups.get(db, group_id)
        if not group:
            raise NotFound("Group not found")

        user = self._users.get_or_create(db, username)
        self._memberships.ensure_membership(db, user.id, group_id)

        return {"groupId": group_id, "username": username}