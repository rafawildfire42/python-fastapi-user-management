import json
import logging

from fastapi import status

from src.database.base import SessionLocal
from src.apps.routes.schemas import RouteBase
from src.tests_base import authenticated_client
from src.apps.permissions_groups.crud import create_permissions_group, delete_permissions_group
from src.apps.permissions.crud import create_permission, delete_permission
from src.apps.routes.crud import create_route, delete_route
from src.apps.permissions_groups.schemas import PermissionGroup
from src.apps.permissions.schemas import PermissionBase

db = SessionLocal()

# ID do usuário de test criado e deletado durante a fase de teste
permissions_group_id = 0
permission_id = 0
test_route_id = 0


def test_request_create_permissions_groups_and_permission_relation():
    # Criando rota de teste
    route_data: dict[str, str | bool] = {
        "path": "/test_permission",
        "needs_permission": True
    }
    test_route = create_route(db, RouteBase.model_validate((route_data)))
    global test_route_id
    test_route_id = test_route.id
    db.close()
    
    permissions_group_data = PermissionGroup.model_validate({
        "name": "permissions_group_test"
    })
    
    
    permission_data = PermissionBase.model_validate({
        "route_id": test_route_id,
        "action": "create"
    })
    
    
    permissions_group = create_permissions_group(db, permissions_group_data)
    permission = create_permission(db, permission_data)
    
    global permissions_group_id
    global permission_id
    
    permissions_group_id = permissions_group.id
    permission_id = permission.id

    data = {
        "permission_id": permission_id,
        "permission_group_id": permissions_group_id
    }
    data = json.dumps(data)

    response = authenticated_client.post("/permissions-and-groups", content=data)
    
    assert response.status_code == status.HTTP_200_OK


def test_request_list_a_permissions_group_and_permission_relation():
    response = authenticated_client.get(f"/permissions-and-groups")

    assert response.status_code == status.HTTP_200_OK


def test_request_delete_permission():
    response = authenticated_client.delete(f"/permissions-and-groups/?permission_id={permission_id}&permissions_group_id={permissions_group_id}")
    
    delete_route(db, test_route_id)
    delete_permission(db, permission_id)
    delete_permissions_group(db, permissions_group_id)

    assert response.status_code == status.HTTP_200_OK
