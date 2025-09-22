from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse

from api.models import (TaskBody, TaskResponse, GetAllTasksResponse, PostTaskResponse,
                        GetSingleTaskResponse, PutTaskResponse)
from api.utils import get_item_by_id, get_item_index_by_id


tasks_data = [
    {"id": 1, "description": "Learn FastAPI", "priority": 3, "is_completed": True},
    {"id": 2, "description": "Do exercises", "priority": 2, "is_completed": False}
]

router = APIRouter(prefix="/tasks")


@router.get("", tags=["tasks"], description="Get all tasks", response_model=GetAllTasksResponse)
def get_tasks():
    response_tasks_data = [
        TaskResponse(task_id=task["id"],
                     description=task["description"],
                     priority=task["priority"],
                     is_completed=task["is_completed"])
        for task in tasks_data
    ]

    return {"result": response_tasks_data}


@router.get("/{task_id}", tags=["tasks"], response_model=GetSingleTaskResponse)
def get_task_by_id(task_id: int):
    target_task = get_item_by_id(tasks_data, task_id)
    if not target_task:
        message = {"error": f"Task with id {task_id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    response_target_task = TaskResponse(
        task_id=target_task["id"],
        description=target_task["description"],
        priority=target_task["priority"],
        is_completed=target_task["is_completed"]
    )
    return {"result": response_target_task}


@router.post("", tags=["tasks"], status_code=status.HTTP_201_CREATED,
             response_model=PostTaskResponse)
def create_task(body: TaskBody):
    new_task: dict = body.model_dump()
    new_task_id: int = max(task["id"] for task in tasks_data) + 1
    new_task["id"] = new_task_id
    tasks_data.append(new_task)

    response_new_task = TaskResponse(
        task_id=new_task["id"],
        description=new_task["description"],
        priority=new_task["priority"],
        is_completed=new_task["is_completed"],
    )

    return {"message": "New task added", "details": response_new_task}


@router.delete("/{task_id}", tags=["tasks"])
def delete_task_by_id(task_id: int):
    target_index = get_item_index_by_id(tasks_data, task_id)
    if target_index is None:
        message = {"error": f"Task with id {task_id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)
    tasks_data.pop(target_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{task_id}", tags=["tasks"], response_model=PutTaskResponse)
def update_task(task_id:int, body: TaskBody):
    target_index = get_item_index_by_id(tasks_data, task_id)

    if target_index is None:
        message = {"error": f"Task with id {task_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)

    updated_task: dict = body.model_dump()
    updated_task["id"] = task_id
    tasks_data[target_index] = updated_task

    response_updated_task = TaskResponse(
        task_id=updated_task["id"],
        description=updated_task["description"],
        priority=updated_task["priority"],
        is_completed=updated_task["is_completed"],
    )

    message = {"message": f"Task with id {task_id} updated",
               "new_value": response_updated_task}
    return message
