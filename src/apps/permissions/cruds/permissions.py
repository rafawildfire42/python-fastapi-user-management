from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def get_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Permission).offset(skip).limit(limit).all()


def get_permission(db, permission_id: int):
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()


def delete_permission(db, permission_id: int):
    db_permission = db.query(models.Permission).filter(
        models.Permission.id == permission_id).first()

    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(db_permission)
    db.commit()

    response_body = {"message": f"Permission #{permission_id} deleted."}

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)


def create_permission(db, permission):
    try:
        db_permission = models.Permission(
            route_id=permission.route_id, action=permission.action.value)
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="This permission has been created or does not have routes with this ID.")


def update_permission(db: Session, permission: schemas.Permission, id: int):
    db_permission = db.query(models.Permission).filter(
        models.Permission.id == id).first()

    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    for field, value in permission.model_dump(exclude_unset=True).items():
        if isinstance(value, schemas.Action):
            setattr(db_permission, field, value.value)
            continue
        setattr(db_permission, field, value)

    db.commit()
    db.refresh(db_permission)

    return db_permission
