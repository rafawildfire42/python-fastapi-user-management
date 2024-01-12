from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint

from src.database.base import Base


permission_association = Table(
    "permission_association",
    Base.metadata,
    Column("permission_id", Integer, ForeignKey("permissions.id")),
    Column("permission_group_id", Integer,
           ForeignKey("permissions_groups.id")),
    UniqueConstraint('permission_id', 'permission_group_id', name='uq_permission_association')
)