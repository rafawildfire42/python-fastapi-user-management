from fastapi import HTTPException, APIRouter, Path, Depends, Body, Query, Request
from typing import Annotated, Optional, List
from sqlalchemy.orm import Session
from src.database.dependencies import get_db
from . import crud
from .schemas import User, UserCreate
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

user_router = APIRouter(prefix="/users", tags=["Users"])
templates = Jinja2Templates(directory="src/apps/users/templates")


@user_router.post("/", response_model=User, summary="Create User")
def create_user(
    user: Annotated[
        UserCreate,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "Create a user",
                    "description": "You will need admin permissions to create an user.",
                    "value": {
                        "username": "rafa@mail.com",
                        "password": "123456",
                    },
                },
                "invalid": {
                    "summary": "Error - Create a user",
                    "description": "Username and password have to be string and username has to be a valid email.",
                    "value": {
                        "username": "rafa",
                        "password": 3242,
                    },
                },
            },
        ),
    ],
    db: Session = Depends(get_db),
):
    """
    Create a new user.

    **Body:**
    - `username`: Field username to create. This field allow only emails pattern.
    - `password`: Field password to create.

    Returns the created user.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@user_router.delete("/{user_id}", response_class=JSONResponse, summary="Delete User")
def delete_user(
    user_id: Annotated[
        int,
        Path(
            title="User ID to delete",
            openapi_examples={
                "normal": {
                    "summary": "Delete a user",
                    "description": "You will need admin permissions to delete an user. Needs to pass a path param.",
                },
            },
        ),
    ],
    db: Session = Depends(get_db),
):
    """
    Delete a user by ID.

    **Path params:**
    - `user_id`: The ID of the user to delete.

    Returns JSON response indicating success.
    """
    return crud.delete_user(db=db, id=user_id)


@user_router.put("/{user_id}", response_model=User, summary="Update User")
def update_user(
    user_id: Annotated[
        int,
        Path(
            title="The ID of the item to get",
            openapi_examples={
                "normal": {
                    "summary": "Update a user",
                    "description": "You will need admin permissions to update an user. You can make partials updates.  Needs to pass a path param.",
                    "value": {
                        "username": "rafa@mail.com",
                    },
                },
                "invalid": {
                    "summary": "Error - Update a user",
                    "description": "Username must be a valid email.",
                    "value": {
                        "username": "rafa",
                    },
                },
            },
        ),
    ],
    user: Optional[User] = None,
    db: Session = Depends(get_db),
):
    """
    Update a user by ID.

    **Path params:**
    - `user_id` : The ID of the user to update.

    **Body:**
    - `email`: Field email to update.
    - `is_active`: Field is_active to update.

    Returns the updated user.
    """
    return crud.update_user(db=db, user=user, id=user_id)


@user_router.get("/", response_model=List[User], summary="List Users")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List users.

    **Path params:**
    - `skip`: Number of users to skip.
    - `limit`: Maximum number of users to retrieve.

    Returns a list of users.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@user_router.get(
    "/confirm-register", response_class=HTMLResponse, summary="Confirm register"
)
def confirm_register(
    request: Request,
    email: Annotated[str | None, Query(max_length=50)],
    db: Session = Depends(get_db),
):
    """
    Confirm register
    
    **Query params:**
    - `email`: Users email.
    
    This endpoint is used to user confirm his register through email

    Returns template for user
    """
    user_data = User()
    user_data.is_active = True
    crud.update_user(db=db, user=user_data, email=email)
    return templates.TemplateResponse(
        request=request, name="confirmed.html", context={"id": id}
    )


@user_router.get("/{user_id}", response_model=User, summary="Get User by ID")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.

    **Path params:**
    - `user_id`: The ID of the user to retrieve.

    Returns the user with the specified ID.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
