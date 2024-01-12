from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from src.apps.permissions.models import Permission
from src.database.base import Base


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    path = Column(String, unique=True, index=True, nullable=False)
    needs_permission = Column(Boolean, index=True, default=True)

    permissions = relationship(Permission, back_populates="route")
