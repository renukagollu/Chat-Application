"""
GroupRepository.

Persistence operations for groups.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.group import Group


class GroupRepository:
    """Repository for group persistence operations."""

    def create(self, db: Session, name: str) -> Group:
        """
        Create and persist a group.

        Args:
            db: SQLAlchemy session.
            name: Group name.

        Returns:
            The created group.
        """
        group = Group(name=name)
        db.add(group)
        db.commit()
        db.refresh(group)
        return group

    def get(self, db: Session, group_id: int) -> Group | None:
        """
        Retrieve a group by ID.

        Args:
            db: SQLAlchemy session.
            group_id: Group identifier.

        Returns:
            Group if found, else None.
        """
        return db.execute(select(Group).where(Group.id == group_id)).scalar_one_or_none()

    def list(self, db: Session) -> list[Group]:
        """
        List groups in reverse creation order.

        Args:
            db: SQLAlchemy session.

        Returns:
            List of groups.
        """
        return list(db.execute(select(Group).order_by(Group.id.desc())).scalars().all())