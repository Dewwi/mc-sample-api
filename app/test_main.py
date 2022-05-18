from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_get_doc():
    response = client.get("/docs")
    assert response.status_code == 200


def test_delete_account():
    raise Exception(client.delete('/accounts/1?deleted=true').json())
   