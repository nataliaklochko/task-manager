from pydantic import BaseModel

from src.usecases.models import Status, Task


class CreateTaskRequest(BaseModel):
    user_id: int
    title: str
    description: str | None = None


class UpdateTaskRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None


class ListTaskRequest(BaseModel):
    user_id: int


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    status: Status

    @classmethod
    def from_entity(cls, task: Task):
        return cls(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            status=task.status,
        )
