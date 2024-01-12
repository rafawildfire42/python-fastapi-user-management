from typing import Annotated
from sqlalchemy.orm import Session

from . import crud
from .schemas import RouteBase, Route as RouteSchema
from src.database.dependencies import get_db

from fastapi import APIRouter, Path, Depends, HTTPException, Body
from fastapi.responses import JSONResponse


routes_router = APIRouter(prefix="/routes", tags=["Routes"])


@routes_router.get("/", response_model=list[RouteSchema])
def read_routes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read a list of routes.

    - **Parameters:**
      - `skip` (int): Number of items to skip in the list.
      - `limit` (int): Maximum number of items to retrieve.

    - **Response:**
      - List of `RouteSchema`.

    """
    return crud.get_routes(db, skip=skip, limit=limit)


@routes_router.get("/{route_id}", response_model=RouteSchema)
def read_route(route_id: int, db: Session = Depends(get_db)):
    """
    Read a specific route.

    - **Parameters:**
      - `route_id` (int): ID of the route to retrieve.

    - **Response:**
      - `RouteSchema` for the specified route.

    - **Raises:**
      - 404: If the route is not found.

    """
    route: RouteSchema | None = crud.get_route(db, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Permission not found")
    return route


@routes_router.delete("/{route_id}", response_class=JSONResponse)
def delete_route(route_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific route.

    - **Parameters:**
      - `route_id` (int): ID of the route to delete.

    - **Response:**
      - JSONResponse.

    """
    return crud.delete_route(db, route_id)


@routes_router.post("/", response_model=RouteSchema)
def create_route(
    route: Annotated[
        RouteBase,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "Create a route",
                    "description": "You will need admin permissions to create a route.",
                    "value": {"path": "/my-route", "needs_permission": True},
                },
                "invalid": {
                    "summary": "Error - Create a route",
                    "description": "needs_permission must be boolean.",
                    "value": {
                        "path": "/rafa",
                        "needs_permission": "true",
                    },
                },
            },
        ),
    ],
    db: Session = Depends(get_db),
):
    """
    Create a new route.

    - **Parameters:**
      - `route` (RouteBase): Data to create a new route.

    - **Response:**
      - `RouteBase` for the newly created route.

    """
    return crud.create_route(db=db, route=route)


@routes_router.put("/{route_id}", response_model=RouteBase)
def update_route(
    route_id: Annotated[int, Path(title="The ID of the item to get")],
    route: RouteBase = None,
    db: Session = Depends(get_db),
):
    """
    Update a specific route.

    - **Parameters:**
      - `route_id` (int): ID of the route to update.
      - `route` (RouteBase): Data to update the route.

    - **Response:**
      - `RouteBase` for the updated route.

    """
    return crud.update_route(db=db, route=route, id=route_id)
