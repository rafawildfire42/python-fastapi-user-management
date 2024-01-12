from sqlalchemy import Table, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from src.database.base import Base
from src.apps.many_to_many.permissions_groups_and_permissions.models import permission_association

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    action = Column(String, index=True, nullable=False)

    route = relationship("Route", back_populates="permissions")
    permissions_group = relationship(
        "PermissionGroup", secondary=permission_association, back_populates="permissions")

    __table_args__ = (
        UniqueConstraint("route_id", "action", name="uq_action_path"),
    )