from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..permissions import models, schemas
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def get_permissions_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PermissionGroup).offset(skip).limit(limit).all()


def get_permissions_group(db, permissions_group_id: int):
    return db.query(models.PermissionGroup).filter(models.PermissionGroup.id == permissions_group_id).first()


def delete_permissions_group(db, permission_groups_id: int):
    db_permissions_group = db.query(models.PermissionGroup).filter(
        models.PermissionGroup.id == permission_groups_id).first()

    if not db_permissions_group:
        raise HTTPException(
            status_code=404, detail="Permission group not found")

    db.delete(db_permissions_group)
    db.commit()

    response_body = {
        "message": f"Permission group #{permission_groups_id} deleted."}

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)


def create_permissions_group(db, permissions_group):
    try:
        db_permissions_group = models.PermissionGroup(
            name=permissions_group.name)
        db.add(db_permissions_group)
        db.commit()
        db.refresh(db_permissions_group)
        return db_permissions_group
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="This permission group has been created or does not have routes with this ID.")


def update_permissions_group(db: Session, permissions_group: schemas.PermissionGroup, id: int):
    db_permissions_group = db.query(models.PermissionGroup).filter(
        models.PermissionGroup.id == id).first()

    if not db_permissions_group:
        raise HTTPException(
            status_code=404, detail="Permission group not found")

    for field, value in permissions_group.model_dump(exclude_unset=True).items():
        if isinstance(value, schemas.Action):
            setattr(db_permissions_group, field, value.value)
            continue
        setattr(db_permissions_group, field, value)

    db.commit()
    db.refresh(db_permissions_group)

    return db_permissions_group
