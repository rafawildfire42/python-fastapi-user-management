import json

from fastapi import status

from src.database.base import SessionLocal
from src.apps.routes.schemas import RouteBase
from src.tests_base import authenticated_client
from src.apps.routes.crud import create_route, delete_route


db = SessionLocal()

# ID do usuário de test criado e deletado durante a fase de teste
permission_id = 0
test_route_id = 0

def test_request_create_permission():
    # Criando rota de teste
    route_data: dict[str, str | bool] = {
        "path": "/test_permission",
        "needs_permission": True
    }
    test_route = create_route(db, RouteBase.model_validate((route_data)))
    global test_route_id
    test_route_id = test_route.id
    db.close()
    
    assert isinstance(test_route_id, int)
    
    data = {
      "route_id": test_route_id,
      "action": "create"
    }
    data = json.dumps(data)

    response = authenticated_client.post("/permissions", content=data)
    
    global permission_id
    permission_id = response.json().get("id")
    
    assert response.status_code == 200
    
def test_request_creating_duplicated_permission():
    data = {
      "route_id": test_route_id,
      "action": "create"
    }
    data = json.dumps(data)

    response = authenticated_client.post("/permissions", content=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    
def test_request_retrieve_a_permission():
    response = authenticated_client.get(f"/permissions/{permission_id}")
    
    assert response.status_code == 200


def test_request_list_permissions():
    response = authenticated_client.get("/permissions")
    
    assert response.status_code == 200


def test_request_update_permission():
    data = {
        "needs_permission": False,
    }
    data = json.dumps(data)
    
    response = authenticated_client.put(f"/permissions/{permission_id}", content=data)
    
    assert response.status_code == 200


def test_request_delete_permission():
    response = authenticated_client.delete(f"/permissions/{permission_id}")
    delete_route(db, test_route_id)
    
    assert response.status_code == 200