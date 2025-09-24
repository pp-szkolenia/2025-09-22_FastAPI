from pydantic import BaseModel


class TaskBody(BaseModel):
    description: str
    priority: int | None = None
    is_completed: bool = False


class UserBody(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class TaskResponse(BaseModel):
    task_id: int
    description: str
    priority: int | None
    is_completed: bool


class GetSingleTaskResponse(BaseModel):
    result: TaskResponse


class GetAllTasksResponse(BaseModel):
    result: list[TaskResponse]


class PostTaskResponse(BaseModel):
    message: str
    details: TaskResponse


class PutTaskResponse(BaseModel):
    message: str
    new_value: TaskResponse


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
