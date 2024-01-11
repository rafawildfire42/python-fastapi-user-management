from fastapi.testclient import TestClient
from .main import app

unauthenticated_client = TestClient(
    app,
    base_url="http://localhost:8000/",
    raise_server_exceptions=True,
)


def get_headers_with_valid_token() -> dict[str, str]:
    user_data = {
        "username": "admin@mail.com",
        "password": "123456"
    }
    response = unauthenticated_client.post("/auth", data=user_data)
    
    token = response.json().get("access_token")
    
    headers = {
      "Authorization": f"Bearer {token}" 
    }
    
    return headers


headers = get_headers_with_valid_token()


authenticated_client = TestClient(
    app,
    base_url="http://localhost:8000/",
    raise_server_exceptions=True,
    headers=headers,
)
