from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class TaskBody(BaseModel):
    description: str
    priority: int | None = None
    is_completed: bool = False


tasks_data = [
    {"id": 1, "description": "Learn FastAPI", "priority": 3, "is_completed": True},
    {"id": 2, "description": "Do exercises", "priority": 2, "is_completed": False}
]

users_data = [
    {"id": 1, "username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"id": 2, "username": "Andżela", "password": "hasło1!", "is_admin": False},
]


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/tasks")
def get_tasks():
    return {"result": tasks_data}


@app.get("/users")
def get_users():
    return {"result": users_data}


@app.post("/tasks")
def create_task(body: TaskBody):
    new_task: dict = body.model_dump()
    new_task_id: int = max(task["id"] for task in tasks_data) + 1
    new_task["id"] = new_task_id
    tasks_data.append(new_task)
    return {"message": "New task added", "details": new_task}
