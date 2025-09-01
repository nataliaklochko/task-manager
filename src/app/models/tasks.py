from pydantic import BaseModel
from uuid import UUID

from src.usecases.models import Status, Task


class CreateTaskRequest(BaseModel):
    title: str
    user_id: UUID
    description: str | None = None


class UpdateTaskRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None


class ListTaskRequest(BaseModel):
    user_id: UUID


class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
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
