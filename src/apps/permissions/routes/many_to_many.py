from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.dependencies import get_db
from src.apps.permissions.cruds import many_to_many
from ..schemas import UserAndGroupRelation, PermissionAndGroupRelation


permissions_and_groups_router = APIRouter(
    prefix="/permissions-and-groups", tags=["Relation between Groups and Permissions - Only Read"])


@permissions_and_groups_router.get("/", response_model=list[PermissionAndGroupRelation])
def read_permissions_and_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List relations between permissions and gorups

    - **Response:**
      - All the permissions

    """
    return many_to_many.get_permissions_and_group_relation(db, skip=skip, limit=limit)


users_and_groups_router = APIRouter(
    prefix="/users-and-groups", tags=["Relation between Groups and Users - Only Read"])


@users_and_groups_router.get("/", response_model=list[UserAndGroupRelation])
def read_users_and_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List relations between users and gorups

    - **Response:**
      - All the permissions

    """
    return many_to_many.get_user_permissions_group_relation(db, skip=skip, limit=limit)
