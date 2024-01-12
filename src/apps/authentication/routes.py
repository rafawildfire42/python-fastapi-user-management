from jose.exceptions import JWTError
from typing import Annotated, Any

from .schemas import (
    Token,
    RefreshToken,
    authenticate_user_and_get_user_id,
    decode_jwt_token,
    get_access_and_refresh_tokens,
)
from src.apps.many_to_many.permissions_groups_and_permissions.crud import (
    get_permissions_and_group_relation,
)
from src.apps.many_to_many.permissions_groups_and_users.crud import get_user_permissions_group_relation_filter
from src.apps.permissions.crud import get_permissions
from src.apps.routes.crud import get_routes
from src.database.dependencies import get_db

from fastapi import Depends, HTTPException, APIRouter, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_data(db_session, email, user_id):
    user_and_group_relation = get_user_permissions_group_relation_filter(
        db_session, user_id
    )
    groups_ids = [item[1] for item in user_and_group_relation]

    permissions_and_group_relation = get_permissions_and_group_relation(
        db_session)
    groups_permissions = list(
        filter(lambda x: x[1] in groups_ids, permissions_and_group_relation)
    )

    permissions_id = list(set([item[0] for item in groups_permissions]))
    all_permissions = get_permissions(db_session)
    my_permissions = list(
        filter(
            lambda x: x.get("id") in permissions_id, jsonable_encoder(
                all_permissions)
        )
    )

    # my_routes_id = list(set([item.get("route_id") for item in my_permissions]))

    all_routes = jsonable_encoder(get_routes(db_session))
    allowed_routes = [
        route.get("path")
        for route in list(
            filter(lambda x: x.get("needs_permission") == False, all_routes)
        )
    ]

    user_permissions = {"create": [], "view": [], "delete": [], "update": []}

    for permission in my_permissions:
        x = list(
            filter(lambda x: x.get("id") ==
                   permission.get("route_id"), all_routes)
        )[0]
        user_permissions[permission.get("action")].append(x.get("path"))

    return {
        "email": email,
        "user_id": user_id,
        "permissions": user_permissions,
        "allowed_routes": allowed_routes,
    }


@auth_router.post("/", response_model=None)
async def login_for_access_token(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    db_session: Any = Depends(get_db),
) -> Token | HTTPException:
    """
    Login.

    **Body:**
    - `username`: Field username to create. This field allow only emails pattern.
    - `password`: Field password to create.

    Returns access_token and refresh_token
    """
    user_id = authenticate_user_and_get_user_id(
        db_session, form_data.username, form_data.password
    )

    data = get_data(db_session, form_data.username, user_id)

    tokens = get_access_and_refresh_tokens(data)

    return {**tokens, "token_type": "bearer"}


@auth_router.post("/refresh-token", response_model=None)
async def refresh_tokens(
    data: Annotated[
        RefreshToken,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "Refresh Token",
                    "description": "You can use refresh token to get another access token.",
                    "value": {"access_token": "encoded_token"},
                },
            },
        ),
    ],
    db_session: Any = Depends(get_db),
) -> JSONResponse | HTTPException:
    """
    Refresh token.

    **Body:**
    - `refresh_token`: The refresh token received in login.

    Returns access_token and refresh_token
    """

    try:
        token = decode_jwt_token(data.refresh_token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is invalid or expired."
        )

    token_data = {"email": token.get("email"), "user_id": token.get("user_id")}
    data_to_encode = get_data(db_session, **token_data)

    tokens = get_access_and_refresh_tokens(data_to_encode)

    return {**tokens, "token_type": "bearer"}
