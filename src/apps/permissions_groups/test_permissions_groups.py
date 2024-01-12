import json

from src.tests_base import authenticated_client


permissions_group_id = 0


def test_request_create_permissions_group():
    data: dict[str, str] = {
        "name": "test_group",
    }
    data_dumped: str = json.dumps(data)

    response = authenticated_client.post(
        "/permissions-groups", content=data_dumped)
    status_code = response.status_code
    global permissions_group_id
    permissions_group_id = response.json().get("id")

    assert status_code == 200


# def test_request_list_routes():
#     response = authenticated_client.get("/routes")
#     status_code = response.status_code

#     assert status_code == 200


# def test_request_retrieve_route():
#     response = authenticated_client.get(f"/routes/{route_id}")
#     status_code = response.status_code

#     assert status_code == 200


# def test_request_update_route():
#     data = {
#         "path": "/teste3"
#     }
#     data_dumped = json.dumps(data)

#     response = authenticated_client.put(f"/routes/{route_id}", content=data_dumped)
#     status_code = response.status_code

#     assert status_code == 200


# def test_request_delete_route():
#     response = authenticated_client.delete(f"/routes/{route_id}")
#     status_code = response.status_code

#     assert status_code == 200
