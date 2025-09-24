import pytest
import json
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def test_get_users_response_code(client: TestClient):
    resp = client.get("/users")
    assert resp.status_code == 200, "Invalid response status code for GET /users"


def test_get_users_response_format(client: TestClient):
    resp = client.get("/users")
    resp_json = resp.json()
    assert isinstance(resp_json, dict)
    assert "result" in resp_json
    assert isinstance(resp_json["result"], list)


def test_query_param_is_admin(client: TestClient):
    resp = client.get("/users", params={"is_admin": True})
    resp_json = resp.json()
    assert all([user["is_admin"] for user in resp_json["result"]])

def test_query_param_password_length(client: TestClient):
    min_length = 2
    resp = client.get("/users", params={"min_password_length": min_length})
    resp_json = resp.json()
    assert all([min_length <= len(user["password"]) for user in resp_json["result"]])


def test_query_param_sort(client: TestClient):
    resp = client.get("/users", params={"sort_by_username": "asc"})
    resp_json = resp.json()
    all_users = [user["username"] for user in resp_json["result"]]

    assert all(isinstance(user, str) for user in all_users)
