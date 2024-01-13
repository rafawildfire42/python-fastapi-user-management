from sqlalchemy.orm import Session

from .schemas import UserAndGroupRelation
from . import crud
from src.database.dependencies import get_db

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


users_and_groups_router = APIRouter(
    prefix="/users-and-groups", tags=["Relation between Groups and Users - Only Read"])


@users_and_groups_router.get("/", response_model=list[UserAndGroupRelation])
def retrieve_user_and_groups(user_id: int = 0, permissions_group_id: int = 0, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List relations between users and gorups

    - **Response:**
      - All the permissions

    """
    return crud.get_user_permissions_group_relation_filter(db, user_id=user_id, permissions_group_id=permissions_group_id, skip=skip, limit=limit)


@users_and_groups_router.post("/", response_model=UserAndGroupRelation)
def create_users_and_groups(data: UserAndGroupRelation, db: Session = Depends(get_db)):
    """
    List relations between users and gorups

    - **Response:**
      - All the permissions

    """
    return crud.create_user_permissions_group_relation(db, data)


@users_and_groups_router.delete("/", response_class=JSONResponse)
def delete_users_and_groups(user_id: int, permissions_group_id: int, db: Session = Depends(get_db)):
    """
    List relations between users and gorups

    - **Response:**
      - All the permissions

    """
    return crud.delete_user_permissions_group_relation(db, user_id=user_id, permissions_group_id=permissions_group_id)

