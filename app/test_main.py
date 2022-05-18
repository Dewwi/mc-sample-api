from fastapi.testclient import TestClient
import pytest
from .main import app

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client 

def _account_exists(test_app, account_id):
    get_response = test_app.get(f'/accounts/{account_id}')
    raise Exception(account_id)
    return True if get_response.status_code == 200 else False

#DOCS
def test_get_doc(test_app):
    response = test_app.get("/docs")
    assert response.status_code == 200

#GET
def test_read_account_not_exists(test_app):
    response = test_app.get('/accounts/1')
    assert response.status_code == 404

#CREATE
def test_create_empty_account(test_app):
    response = test_app.post(
        '/accounts',
        headers={},
        json={}
    )
    assert response.status_code == 200
    assert 'id' in response.json()
    ## This portion won't work since the data isn't persisted
    response = test_app.get('/accounts/0')
    assert response.status_code == 200

#PATCH
def test_patch_account(test_app):
    response = test_app.patch(
        '/accounts/1',
        headers={},
        json={"name": "david"}
    )
    assert response.status_code == 200
    assert 'id' in response.json()
    ## This portion won't work since the data isn't persisted
    response = test_app.get('/accounts/0')
    assert response.status_code == 200

#DELETE
def test_delete_account_not_exists(test_app):
    response = test_app.delete('/accounts/1')
    assert response.status_code == 404

def test_delete_account_exists(test_app):
    response = test_app.delete('/accounts/1')
    assert response.status_code == 200
    ## This portion won't work since the data isn't persisted




   