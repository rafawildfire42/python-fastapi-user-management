from sqlalchemy.orm import Session
from ...permissions import models


def get_permissions_and_group_relation(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.permission_association).offset(skip).limit(limit).all()
