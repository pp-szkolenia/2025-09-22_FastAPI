
import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def test_post_user(client: TestClient):
    payload = {"username": "Test update pytest", "password": "asdfghjkl;", "is_admin": True}
    resp = client.post("/users", json=payload)
    resp_json = resp.json()
    assert resp.status_code == 201, "Invalid response status code for POST /users"
    assert "message" in resp_json and "details" in resp_json
