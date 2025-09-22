from fastapi.testclient import TestClient

from api.main import app

with TestClient(app) as client:
    # GET /tasks
    resp = client.get("/tasks")
    assert resp.status_code == 200, "Invalid response status code for GET /tasks"
    resp_json = resp.json()
    assert "result" in resp_json.keys(), "GET /tasks should return a JSON with 'result' key"

    # POST /tasks
    payload = {"description": "Opis", "is_completed": True, "priority": 2}
    resp = client.post("/tasks", json=payload)

    assert resp.status_code in (200, 201), "Invalid response status code for POST /tasks"
    resp_json = resp.json()
    assert "message" in resp_json.keys() and "details" in resp_json.keys()
    assert isinstance(resp_json["details"], dict)
