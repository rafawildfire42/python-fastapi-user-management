from sqlalchemy.orm import Session
from ...permissions import models


def get_permissions_and_group_relation(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.permission_association).offset(skip).limit(limit).all()


def get_user_permissions_group_relation(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.permissions_group_user_association).offset(skip).limit(limit).all()


def get_user_permissions_group_relation_filter(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.permissions_group_user_association).filter_by(user_id=user_id).all()
