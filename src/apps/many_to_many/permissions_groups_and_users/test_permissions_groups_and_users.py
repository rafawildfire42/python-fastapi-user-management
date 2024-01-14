import json
import logging

from fastapi import status

from src.database.base import SessionLocal
from src.apps.routes.schemas import RouteBase
from src.apps.users.crud import create_user, delete_user
from src.tests_base import authenticated_client
from src.apps.permissions_groups.crud import create_permissions_group, delete_permissions_group
from src.apps.permissions.crud import create_permission, delete_permission
from src.apps.routes.crud import create_route, delete_route
from src.apps.permissions_groups.schemas import PermissionGroup
from src.apps.users.schemas import UserCreate

db = SessionLocal()

permissions_group_id = 0
user_id = 0


def test_request_list_permissions_group_and_users_relation():
    response = authenticated_client.get(f"/users-and-groups")

    assert response.status_code == status.HTTP_200_OK


def test_request_create_permissions_group_and_users_relation():
    global permissions_group_id
    global user_id

    user_data = UserCreate.model_validate({
        "email": "rafaondjango@gmail.com",
        "password": "123456"
    })

    db_user = create_user(db, user_data)
    user_id = db_user.id

    permissions_group_data = PermissionGroup.model_validate({
        "name": "permissions_group_test"
    })
    db_permissions_group = create_permissions_group(db, permissions_group_data)
    permissions_group_id = db_permissions_group.id

    request_data_dict = {
        "permission_group_id": permissions_group_id,
        "user_id": user_id
    }
    request_data = json.dumps(request_data_dict)

    response = authenticated_client.post(
        "/users-and-groups", content=request_data)

    assert response.status_code == status.HTTP_200_OK


def test_request_delete_permissions_group_and_user_relation():

    response = authenticated_client.delete(
        f"/users-and-groups/?user_id={user_id}&permissions_group_id={permissions_group_id}")

    delete_user(db, user_id)
    delete_permissions_group(db, permissions_group_id)

    assert response.status_code == status.HTTP_200_OK
