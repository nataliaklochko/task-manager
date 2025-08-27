from pydantic import BaseModel
from uuid import UUID

from src.usecases.models import Status, Task


class TaskCreateRequest(BaseModel):
    title: str
    user_id: UUID
    description: str | None = None


class TaskUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None


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
