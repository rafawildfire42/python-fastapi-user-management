from fastapi import APIRouter, Path, Depends, HTTPException, Body
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from src.database.dependencies import get_db
from src.apps.permissions.cruds import permissions
from ..schemas import Permission, PermissionBase

permissions_router = APIRouter(prefix="/permissions", tags=["Permissions"])


@permissions_router.get("/", response_model=list[Permission])
def read_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read a list of permissions.

    - **Query params:**
      - `skip`: Number of items to skip in the list.
      - `limit`: Maximum number of items to retrieve.

    - **Response:**
      - List of `Permission`.

    """
    return permissions.get_permissions(db, skip=skip, limit=limit)


@permissions_router.get("/{permission_id}", response_model=Permission)
def read_permission(permission_id: int, db: Session = Depends(get_db)):
    """
    Read a specific permission.

    - **Path params:**
      - `permission_id`: ID of the permission to retrieve.

    - **Response:**
      - `Permission` for the specified permission.

    - **Raises:**
      - 404: If the permission is not found.

    """
    permission: Permission | None = permissions.get_permission(
        db, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


@permissions_router.delete("/{permission_id}", response_class=JSONResponse)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific permission.

    - **Path params:**
      - `permission_id`: ID of the permission to delete.

    - **Response:**
      - JSONResponse.

    """
    return permissions.delete_permission(db, permission_id)


@permissions_router.post("/", response_model=PermissionBase)
def create_permission(
    permission: Annotated[
        PermissionBase,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "Create a route",
                    "description": "You will need admin permissions to create a route. Have to pass the route id and its action (create, view(read), update, delete)",
                    "value": {"route_id": 13, "action": "create"},
                },
                "invalid": {
                    "summary": "Error - Create a route",
                    "description": "The path params must be the route_id and not the path and the action has to be one of this (create, view, delete, update).",
                    "value": {
                        "path": "/rafa",
                        "action": "/patch",
                    },
                },
            },
        ),
    ],
    db: Session = Depends(get_db),
):
    """
    Create a new permission.

    - **Body:**
      - `route_id`: Route to associate the permission.
      - `action`: What can do in this route.

    - **Response:**
      - `PermissionBase` for the newly created permission.

    """
    return permissions.create_permission(db=db, permission=permission)


@permissions_router.put("/{permission_id}", response_model=PermissionBase)
def update_permission(
    permission_id: Annotated[int, Path(title="The ID of the item to get")],
    permission: PermissionBase = None,
    db: Session = Depends(get_db),
):
    """
    Update a specific permission.

    - **Path params:**
      - `permission_id`: ID of the permission to update.
      
    - **Body:**
      - `route_id`: Route to associate the permission.
      - `action`: What can do in this route.

    - **Response:**
      - `PermissionBase` for the updated permission.

    """
    return permissions.update_permission(db=db, permission=permission, id=permission_id)
