import logging
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Relationship, Session
from sqlalchemy.orm.exc import FlushError

from . import models
from .schemas import PermissionAndGroupRelation
from src.apps.permissions_groups.crud import get_permissions_group
from src.apps.permissions.crud import get_permission

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


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


def create_user_permissions_group_relation(db: Session, data: PermissionAndGroupRelation):
    permissions_group_id = data.permission_group_id
    permission_id = data.permission_id

    try:
        db_permission = get_permission(db, permission_id=permission_id)
        db_permissions_group = get_permissions_group(
            db, permissions_group_id=permissions_group_id)
        db_permission.permissions_group.append(db_permissions_group)
        db.commit()
        return db.query(models.permission_association).filter_by(permission_id=permission_id, permission_group_id=permissions_group_id).first()

    except (FlushError, AttributeError) as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Error while creating relation between permissions groups and user. Check if Permissions Group #{permissions_group_id} and Permission #{permission_id} exists.")

    except IntegrityError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Relation between Permissions Group #{permissions_group_id} and Permission #{permission_id} already exists.")

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Error while creating relation between Permissions Group #{permissions_group_id} and Permission #{permission_id}.")
