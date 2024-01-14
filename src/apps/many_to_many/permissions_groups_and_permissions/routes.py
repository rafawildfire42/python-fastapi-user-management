from sqlalchemy.orm import Session

from .schemas import PermissionAndGroupRelation
from src.apps.many_to_many.permissions_groups_and_permissions import crud
from src.database.dependencies import get_db

from fastapi import APIRouter, Depends


permissions_and_groups_router = APIRouter(
    prefix="/permissions-and-groups", tags=["Relation between Groups and Permissions - Only Read"])


@permissions_and_groups_router.get("/", response_model=list[PermissionAndGroupRelation])
def get_permission_and_permissions_group_relation(permission_id: int = 0, permissions_group_id: int = 0, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List relations between permissions and gorups

    - **Response:**
      - All the permissions

    """
    return crud.get_permission_and_permissions_group_relation(db, permission_id=permission_id, permissions_group_id=permissions_group_id, skip=skip, limit=limit)


@permissions_and_groups_router.post("/", response_model=PermissionAndGroupRelation)
def create_permissions_group_and_permissions_relation(data: PermissionAndGroupRelation, db: Session = Depends(get_db)):
    """
    List relations between permissions and gorups

    - **Response:**
      - All the permissions

    """
    return crud.create_permissions_group_and_permissions_relation(db, data=data)


@permissions_and_groups_router.delete("/", response_model=PermissionAndGroupRelation)
def delete_permissions_and_groups(permission_id: int, permissions_group_id: int, db: Session = Depends(get_db)):
    """
    List relations between permissions and gorups

    - **Response:**
      - All the permissions

    """
    return crud.delete_permissions_group_and_permission_relation(db, permission_id=permission_id, permissions_group_id=permissions_group_id)
