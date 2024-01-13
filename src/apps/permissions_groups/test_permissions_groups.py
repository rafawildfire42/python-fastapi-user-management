import json

from src.tests_base import authenticated_client

from fastapi import Response, status


permissions_group_id: int = 0


def test_request_create_permissions_group() -> None:
    data: dict[str, str] = {
        "name": "test_group",
    }
    data_dumped: str = json.dumps(data)

    response: Response = authenticated_client.post(
        "/permissions-groups", content=data_dumped)
    status_code: int = response.status_code
    global permissions_group_id
    permissions_group_id = response.json().get("id")

    assert status_code == status.HTTP_200_OK


def test_request_list_permissions_groups() -> None:
    response: Response = authenticated_client.get("/permissions-groups")
    status_code: int = response.status_code

    assert status_code == status.HTTP_200_OK


def test_request_retrieve_permissions_group():
    response: Response = authenticated_client.get(f"/permissions-groups/{permissions_group_id}")
    status_code: int = response.status_code

    assert status_code == status.HTTP_200_OK


def test_request_update_permissions_group():
    data = {
        "name": "test_group_updated"
    }
    data_dumped: str = json.dumps(data)

    response = authenticated_client.put(f"/permissions-groups/{permissions_group_id}", content=data_dumped)
    status_code: int = response.status_code

    assert status_code == status.HTTP_200_OK


def test_request_delete_route():
    response = authenticated_client.delete(f"/permissions-groups/{permissions_group_id}")
    status_code: int = response.status_code

    assert status_code == status.HTTP_200_OK
