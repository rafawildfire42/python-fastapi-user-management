from src.base import authenticated_client
import json

def test_request_retrieve_a_user():
    userd_id_to_retrieve = 1
    response = authenticated_client.get(f"/users/{userd_id_to_retrieve}")
    assert response.status_code == 200


def test_request_list_users():
    response = authenticated_client.get("/users")
    assert response.status_code == 200


def test_request_create_user():
    data = {
        "email": "rafaondjango@gmail.com",
        "password": "123456"
    }
    data = json.dumps(data)
    
    response = authenticated_client.post("/users", content=data)
    user_id = response.json().get("id")
    response = authenticated_client.delete(f"/users/{user_id}")
    
    assert response.status_code == 200