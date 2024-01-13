from sqlalchemy.orm import Session

from . import models


def get_permission_and_permissions_group_relation(db: Session, permission_id: int = 0, permissions_group_id: int = 0, skip: int = 0, limit: int = 100):
    db_query = db.query(models.permission_association)

    if permission_id and permissions_group_id:
        return db_query.filter_by(permission_id=permission_id, permission_group_id=permissions_group_id).all()
    elif permission_id or permissions_group_id:
        if permissions_group_id:
            return db_query.filter_by(permission_group_id=permissions_group_id).all()
        else:
            return db_query.filter_by(permission_id=permission_id).all()
    else:
        return db_query.offset(skip).limit(limit).all()