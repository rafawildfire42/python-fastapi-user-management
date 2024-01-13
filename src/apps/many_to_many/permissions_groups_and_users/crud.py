import logging
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Relationship, Session
from sqlalchemy.orm.exc import FlushError

from . import models
from .schemas import UserAndGroupRelation
from src.apps.permissions_groups.crud import get_permissions_group
from src.apps.users.crud import get_user_by_id

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def get_user_permissions_group_relation(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.permissions_group_user_association).offset(skip).limit(limit).all()


def get_user_permissions_group_relation_filter(db: Session, user_id: int = 0, permissions_group_id: int = 0, skip: int = 0, limit: int = 100):
    db_query = db.query(models.permissions_group_user_association)
    
    if user_id and permissions_group_id:
        return db_query.filter_by(user_id=user_id, permission_group_id=permissions_group_id).all()
    elif user_id or permissions_group_id:
        if permissions_group_id:
            return db_query.filter_by(permission_group_id=permissions_group_id).all()
        else:
            return db_query.filter_by(user_id=user_id).all()
    else:
        return db_query.offset(skip).limit(limit).all()


def create_user_permissions_group_relation(db: Session, data: UserAndGroupRelation):
    permissions_group_id = data.permission_group_id
    user_id = data.user_id
    
    try:
        db_user = get_user_by_id(db, id=user_id)
        db_permissions_group = get_permissions_group(db, permissions_group_id=permissions_group_id)
        db_user.permissions_group.append(db_permissions_group)
        db.commit()
        return db.query(models.permissions_group_user_association).filter_by(user_id=user_id, permission_group_id=permissions_group_id).first()
    
    except (FlushError, AttributeError) as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error while creating relation between permissions groups and user. Check if Permissions Group #{permissions_group_id} and User #{user_id} exists.")
    
    except IntegrityError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Relation between Permissions Group #{permissions_group_id} and User #{user_id} already exists.")
    
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error while creating relation between Permissions Group #{permissions_group_id} and User #{user_id}.")
    

def delete_user_permissions_group_relation(db: Session, user_id: int, permissions_group_id: int):
    stmt = delete(models.permissions_group_user_association).where(
        models.permissions_group_user_association.c.user_id == user_id,
        models.permissions_group_user_association.c.permission_group_id == permissions_group_id
    )

    result = db.execute(stmt)
    deleted_rows = result.rowcount
    
    if not deleted_rows:
        return JSONResponse(content={
            "detail": "No records deleted. Maybe you passed a relation that doesn't exists."
        }, status_code=status.HTTP_400_BAD_REQUEST)
    
    db.commit()

    return JSONResponse(content={
            "detail": "No records deleted. Maybe you passed a relation that doesn't exists."
        }, status_code=status.HTTP_400_BAD_REQUEST)
    
