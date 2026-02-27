"""
MembershipRepository.

Handles user-group membership persistence.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.membership import Membership


class MembershipRepository:
    """Repository for membership operations."""

    def ensure_membership(self, db: Session, user_id: int, group_id: int) -> None:
        """
        Create membership if it doesn't exist.

        Args:
            db: SQLAlchemy session.
            user_id: User ID.
            group_id: Group ID.
        """
        exists = db.execute(
            select(Membership).where(Membership.user_id == user_id, Membership.group_id == group_id)
        ).scalar_one_or_none()
        if exists:
            return

        db.add(Membership(user_id=user_id, group_id=group_id))
        db.commit()

    def is_member(self, db: Session, user_id: int, group_id: int) -> bool:
        """
        Check if a user is a member of a group.

        Args:
            db: SQLAlchemy session.
            user_id: User ID.
            group_id: Group ID.

        Returns:
            True if membership exists, else False.
        """
        m = db.execute(
            select(Membership).where(Membership.user_id == user_id, Membership.group_id == group_id)
        ).scalar_one_or_none()
        return m is not None