from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from src.apps.permissions.models import (
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

    permissions_group = relationship(
        PermissionGroup,
        secondary=permissions_group_user_association,
        back_populates="users",
    )
