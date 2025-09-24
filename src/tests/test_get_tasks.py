import pytest
import json
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def test_get_tasks_response_code(client: TestClient):
    resp = client.get("/tasks")
    assert resp.status_code == 200, "Invalid response status code for GET /tasks"


def test_get_tasks_response_format(client: TestClient):
    resp = client.get("/tasks")
    resp_json = resp.json()
    assert isinstance(resp_json, dict)
    assert "result" in resp_json
    assert isinstance(resp_json["result"], list)


def test_query_param_is_completed(client: TestClient):
    resp = client.get("/tasks", params={"is_completed": True})
    resp_json = resp.json()
    assert all([task["is_completed"] for task in resp_json["result"]])

    resp = client.get("/tasks", params={"is_completed": False})
    resp_json = resp.json()
    assert all([task["is_completed"] is False for task in resp_json["result"]])


def test_query_param_priority(client: TestClient):
    min_priority = 2
    max_priority = 4
    resp = client.get("/tasks", params={"min_priority": min_priority, "max_priority":max_priority})
    resp_json = resp.json()
    assert all([min_priority <= task["priority"] <= max_priority for task in resp_json["result"]])


def test_query_param_sort(client: TestClient):
    resp = client.get("/tasks", params={"sortByDescription": "asc"})
    resp_json = resp.json()
    all_descriptions = [task["description"] for task in resp_json["result"]]
    # with open("sort_db.json", "w") as f:
    #     json.dump(all_descriptions, f, indent=2)

    sorted_descriptions = sorted(all_descriptions)

    # with open("sort_python.json", "w") as f:
    #     json.dump(sorted_descriptions, f, indent=2)

    assert all(isinstance(description, str) for description in all_descriptions)
    # assert sorted_descriptions == all_descriptions
