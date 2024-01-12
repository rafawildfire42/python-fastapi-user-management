from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.dependencies import get_db
from src.apps.many_to_many.permissions_groups_and_permissions import crud
from .schemas import UserAndGroupRelation


users_and_groups_router = APIRouter(
    prefix="/users-and-groups", tags=["Relation between Groups and Users - Only Read"])


@users_and_groups_router.get("/", response_model=list[UserAndGroupRelation])
def read_users_and_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List relations between users and gorups

    - **Response:**
      - All the permissions

    """
    return crud.get_user_permissions_group_relation(db, skip=skip, limit=limit)
