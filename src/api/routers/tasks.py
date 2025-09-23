from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from api.models import (TaskBody, TaskResponse, GetAllTasksResponse, PostTaskResponse,
                        GetSingleTaskResponse, PutTaskResponse)
from api.utils import get_item_by_id, get_item_index_by_id
from db.utils import connect_to_db
from db.orm import get_session
from db.models import Task
from sqlalchemy import select, func, asc, desc


router = APIRouter(prefix="/tasks")


@router.get("", tags=["tasks"], description="Get all tasks", response_model=GetAllTasksResponse)
def get_tasks(session: Session = Depends(get_session)):
    with session:
        stmt = select(Task)
        tasks_data = session.scalars(stmt).all()

    response_tasks_data = [
        TaskResponse(task_id=task.id_number,
                     description=task.description,
                     priority=task.priority,
                     is_completed=task.is_completed)
        for task in tasks_data
    ]
    return {"result": response_tasks_data}


@router.get('/{task_id}', tags=["tasks"], description="Get task by ID")
def get_task_by_id(task_id: int, session: Session = Depends(get_session)):
    with session:
        stmt = select(Task).where(Task.id_number == task_id)
        tasks_data = session.scalars(stmt).first()

    if not tasks_data:
        message = {'error': f'Task with id: {task_id} NOT FOUND'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    tasks_data_response = {
        "id": tasks_data.id_number,
        "description": tasks_data.description,
        "priority": tasks_data.priority,
        "is_completed": tasks_data.is_completed
    }

    msg = {"result": tasks_data_response}
    return msg


@router.post('', status_code=status.HTTP_201_CREATED, tags=["tasks"], description="Create new task")
def create_task(body: TaskBody, session: Session = Depends(get_session)):
    new_task = Task(**body.model_dump())
    with session:
        session.add(new_task)
        session.commit()
        session.refresh(new_task)

    msg = {'message': 'New task added', 'details': new_task}
    return msg


@router.delete('/{task_id}', tags=["tasks"], description="Delete task by ID")
def delete_task_by_id(task_id: int, session: Session = Depends(get_session)):
    with session:
        stmt = select(Task).where(Task.id_number == task_id)
        target_task = session.scalars(stmt).first()

    if not target_task:
        message = {'error': f'User with id: {task_id} NOT FOUND'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    else:
        session.delete(target_task)
        session.commit()

    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.put('/{task_id}', tags=["tasks"], description="Update task by ID")
def update_task(task_id: int, body: TaskBody, session: Session = Depends(get_session)):
    with session:
        stmt = select(Task).where(Task.id_number == task_id)
        target_task = session.scalars(stmt).first()

        if not target_task:
            message = {'error': f'User with id: {task_id} NOT FOUND'}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        else:
            update_task = target_task
            for field, value in body.model_dump().items():
                setattr(update_task, field, value)
            session.commit()

        response_update_task = {
            "user_id": update_task.id_number,
            "description": update_task.description,
            "priority": update_task.priority,
            "is_completed": update_task.is_completed
        }

        message = {
            "message": f"User with id: {task_id} updated",
            "new_value": response_update_task, }
        return message
