from main import app
from base import client

def test_request_retrieve_a_user():
    userd_id_to_retrieve = 1
    
    request = client.get(f"/users/{userd_id_to_retrieve}")
    
    assert request.status_code == 200


