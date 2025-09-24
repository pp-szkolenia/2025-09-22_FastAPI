import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def create_task_and_get_id(client: TestClient):
    payload = {"description": "test for update", "priority": 1,
               "is_completed": True}
    resp = client.post("/tasks", json=payload)
    new_task_id = resp.json()["details"]["id_number"]
    return new_task_id


def get_all_tasks(client: TestClient):
    resp = client.get("/tasks")
    all_ids = [task["task_id"] for task in resp.json()["result"]]
    return all_ids


def test_delete_task(client: TestClient):
    new_task_id = create_task_and_get_id(client)
    resp = client.delete(f"/tasks/{new_task_id}")

    all_ids = get_all_tasks(client)

    assert resp.status_code == 202
    assert new_task_id not in all_ids
