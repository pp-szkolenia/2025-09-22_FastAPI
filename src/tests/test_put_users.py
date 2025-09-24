import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def create_user_and_get_id(client: TestClient):
    payload = {"username": "Pytest PUT", "password": "2qwertyuiop", "is_admin": False}
    resp = client.post("/users", json=payload)
    new_user_id = resp.json()["details"]["id_number"]
    return new_user_id


def test_update_user(client: TestClient):
    new_user_id = create_user_and_get_id(client)

    payload = {"username": "Update User", "password": "234567890", "is_admin": True}
    resp = client.put(f"/users/{new_user_id}", json=payload)
    resp_json_new_value = resp.json()['new_value']

    assert resp.status_code == 200
    assert resp_json_new_value["user_name"] == "Update User"
    assert resp_json_new_value["password"] == "234567890"
    assert resp_json_new_value["is_admin"] is True
