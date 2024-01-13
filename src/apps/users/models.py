from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Relationship, relationship
from typing import Any

from src.apps.many_to_many.permissions_groups_and_users.models import (
    permissions_group_user_association,
)
from src.apps.permissions_groups.models import PermissionGroup
from src.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)

    permissions_group: Relationship[Any] = relationship(
        PermissionGroup,
        secondary=permissions_group_user_association,
        back_populates="users",
    )
