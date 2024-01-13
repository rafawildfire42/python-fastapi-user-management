import logging
from sqlalchemy.orm import Session

from . import models
from .schemas import UserAndGroupRelation
from src.apps.permissions_groups.crud import get_permissions_group
from src.apps.users.crud import get_user_by_id

from fastapi import HTTPException, status


def get_user_permissions_group_relation(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.permissions_group_user_association).offset(skip).limit(limit).all()


def get_user_permissions_group_relation_filter(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.permissions_group_user_association).filter_by(user_id=user_id).all()


def create_user_permissions_group_relation(db: Session, data: UserAndGroupRelation):
    permissions_group_id = data.permission_group_id
    user_id = data.user_id
    
    try:
        db_user = get_user_by_id(db, id=user_id)
        db_permissions_group = get_permissions_group(db, permissions_group_id=permissions_group_id)
        db_user.permissions_group.append(db_permissions_group)
        db.commit()
        return db.query(models.permissions_group_user_association).filter_by(user_id=1).all()
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error while creating relation between permissions group #{permissions_group_id} and user #{user_id}. Check if this relation already exists.")
        
    
