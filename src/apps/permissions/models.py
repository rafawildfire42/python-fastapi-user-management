from sqlalchemy import Table, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from src.database.base import Base


permission_association = Table(
    "permission_association",
    Base.metadata,
    Column("permission_id", Integer, ForeignKey("permissions.id")),
    Column("permission_group_id", Integer,
           ForeignKey("permissions_groups.id")),
    UniqueConstraint('permission_id', 'permission_group_id', name='uq_permission_association')
)


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