import json

from src.tests_base import authenticated_client

# ID do usuário de test criado e deletado durante a fase de teste
user_id = 0


def test_request_create_user():
    data = {
        "email": "rafaondjango@gmail.com",
        "password": "123456"
    }
    data = json.dumps(data)

    response = authenticated_client.post("/users", content=data)

    # Alterando a variável global user_id para o usuário de teste ser utilizado nos demais tests
    global user_id
    user_id = response.json().get("id")

    assert response.status_code == 200


def test_request_retrieve_a_user():
    userd_id_to_retrieve = user_id
    response = authenticated_client.get(f"/users/{userd_id_to_retrieve}")
    assert response.status_code == 200


def test_request_list_users():
    response = authenticated_client.get("/users")
    assert response.status_code == 200


def test_request_update_user():
    data = {
        "is_active": True,
    }
    data = json.dumps(data)

    response = authenticated_client.put(f"/users/{user_id}", content=data)

    assert response.status_code == 200


def test_request_delete_user():
    response = authenticated_client.delete(f"/users/{user_id}")
    assert response.status_code == 200
