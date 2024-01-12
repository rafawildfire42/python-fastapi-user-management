from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint

from src.database.base import Base

permissions_group_user_association = Table(
    "permissions_group_user_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("permission_group_id", Integer,
           ForeignKey("permissions_groups.id")),
    UniqueConstraint('user_id', 'permission_group_id',
                     name='uq_permissions_group_user_association')
)
