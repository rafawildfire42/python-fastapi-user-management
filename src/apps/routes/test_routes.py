import json

from src.tests_base import authenticated_client


route_id = 0


def test_request_create_route():
    data: dict[str, str | bool] = {
        "path": "/test2",
        "needs_permission": True
    }
    data_dumped: str = json.dumps(data)

    response = authenticated_client.post("/routes", content=data_dumped)
    status_code = response.status_code
    global route_id
    route_id = response.json().get("id")

    assert status_code == 200


def test_request_list_routes():
    response = authenticated_client.get("/routes")
    status_code = response.status_code

    assert status_code == 200


def test_request_retrieve_route():
    response = authenticated_client.get(f"/routes/{route_id}")
    status_code = response.status_code

    assert status_code == 200


def test_request_update_route():
    data = {
        "path": "/teste3"
    }
    data_dumped = json.dumps(data)

    response = authenticated_client.put(
        f"/routes/{route_id}", content=data_dumped)
    status_code = response.status_code

    assert status_code == 200


def test_request_delete_route():
    response = authenticated_client.delete(f"/routes/{route_id}")
    status_code = response.status_code

    assert status_code == 200
