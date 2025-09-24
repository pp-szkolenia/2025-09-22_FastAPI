
import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def create_user_and_get_id(client: TestClient):
    payload = {"username": "Pytest", "password": "XYZ123!@#", "is_admin": True}
    resp = client.post("/users", json=payload)
    new_user_id = resp.json()["details"]["id_number"]
    return new_user_id


def get_all_users(client: TestClient):
    resp = client.get("/users")
    all_ids = [user["username"] for user in resp.json()["result"]]
    return all_ids


def test_delete_user(client: TestClient):
    del_user_id = create_user_and_get_id(client)
    resp = client.delete(f"/users/{del_user_id}")

    all_ids = get_all_users(client)
    assert resp.status_code == 202

