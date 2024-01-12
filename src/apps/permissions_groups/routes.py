from typing import Annotated
from sqlalchemy.orm import Session

from src.apps.permissions_groups import crud
from src.apps.permissions_groups.schemas import PermissionGroup, PermissionGroupBase
from src.database.dependencies import get_db

from fastapi import APIRouter, Path, Depends, HTTPException, Body
from fastapi.responses import JSONResponse


permissions_groups_router = APIRouter(
    prefix="/permissions-groups", tags=["Permissions Groups"]
)


@permissions_groups_router.get("/", response_model=list[PermissionGroupBase])
def read_permissions_groups(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Read a list of permission groups.

    - **Query params:**
      - `skip`: Number of items to skip in the list.
      - `limit`: Maximum number of items to retrieve.

    - **Response:**
      - List of `PermissionGroupBase`.

    """
    return crud.get_permissions_groups(db, skip=skip, limit=limit)


@permissions_groups_router.get(
    "/{permission_group_id}", response_model=PermissionGroupBase
)
def read_permissions_group(permission_group_id: int, db: Session = Depends(get_db)):
    """
    Read a specific permission group.

    - **Path params:**
      - `permission_group_id`: ID of the permission group to retrieve.

    - **Response:**
      - `PermissionGroupBase` for the specified permission group.

    - **Raises:**
      - 404: If the permission group is not found.

    """
    permission_group: PermissionGroup | None = crud.get_permissions_group(
        db, permission_group_id
    )
    if not permission_group:
        raise HTTPException(
            status_code=404, detail="Permission group not found")
    return permission_group


@permissions_groups_router.delete(
    "/{permissions_group_id}", response_class=JSONResponse
)
def delete_permissions_group(permissions_group_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific permission group.

    - **Path params:**
      - `permissions_group_id`: ID of the permission group to delete.

    - **Response:**
      - JSONResponse. Information about the delete.

    """
    return crud.delete_permissions_group(db, permissions_group_id)


@permissions_groups_router.post("/", response_model=PermissionGroup)
def create_permissions_group(
    permissions_group: Annotated[
        PermissionGroup,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "Create a route",
                    "description": "Needs to pass only the name of the group as string. You will need admin permissions to create a route.",
                    "value": {"name": "custom_user"},
                },
            },
        ),
    ],
    db: Session = Depends(get_db),
):
    """
    Create a new permission group.

    - **Path params:**
      - `name`: The name of the route like "/users" or "/resource".

    - **Response:**
      - Same of the input

    """
    return crud.create_permissions_group(
        db=db, permissions_group=permissions_group
    )


@permissions_groups_router.put(
    "/{permissions_group_id}", response_model=PermissionGroupBase
)
def update_permissions_group(
    permissions_group_id: Annotated[int, Path(title="The ID of the item to get")],
    permissions_group: PermissionGroupBase = None,
    db: Session = Depends(get_db),
):
    """
    Update a specific permission group.

    - **Path params:**
      - `permissions_group_id`: ID of the permission group to update.

    - **Body:**
      - `name`: Data to update the permission group.

    - **Response:**
      - Information of the data update

    """
    return crud.update_permissions_group(
        db=db, permissions_group=permissions_group, id=permissions_group_id
    )
