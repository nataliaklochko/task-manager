import uuid
from typing import Protocol

from src.usecases.models import Task, User


class IRepository(Protocol):
    async def create_task(self, task: Task) -> Task:
        raise NotImplementedError

    async def get_task(self, user_id: uuid.UUID, task_id: uuid.UUID) -> Task | None:
        raise NotImplementedError

    async def list_tasks(self, user_id: uuid.UUID) -> list[Task]:
        raise NotImplementedError

    async def update_task(self, user_id: uuid.UUID, task: Task) -> Task | None:
        raise NotImplementedError

    async def delete_task(self, user_id: uuid.UUID, task_id: uuid.UUID) -> bool:
        raise NotImplementedError

    async def create_user(self, user: User) -> User:
        raise NotImplementedError

    async def get_user(self, user_id: uuid.UUID) -> User | None:
        raise NotImplementedError

    async def list_users(self) -> list[User]:
        raise NotImplementedError
