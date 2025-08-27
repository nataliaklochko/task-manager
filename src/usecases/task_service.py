import uuid

from src.usecases.models import Task, Status
from src.interfaces.repository import IRepository


class TaskService:
    def __init__(self, repo: IRepository):
        self.repo = repo

    async def create_task(
        self, user_id: uuid.UUID, title: str, description: str | None = None
    ) -> Task:
        task = Task(
            id=uuid.uuid4(),
            user_id=user_id,
            title=title,
            description=description,
            status=Status.created,
        )
        return await self.repo.create_task(task)

    async def get_task(self, user_id: uuid.UUID, task_id: uuid.UUID) -> Task | None:
        return await self.repo.get_task(user_id, task_id)

    async def list_tasks(self, user_id: uuid.UUID) -> list[Task]:
        return await self.repo.list_tasks(user_id)

    async def update_task(
        self,
        user_id: uuid.UUID,
        task_id: uuid.UUID,
        title: str | None = None,
        description: str | None = None,
        status: Status | None = None,
    ) -> Task | None:
        task = await self.repo.get_task(user_id, task_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status

        return await self.repo.update_task(user_id=user_id, task=task)

    async def delete_task(self, user_id: uuid.UUID, task_id: uuid.UUID) -> bool:
        return await self.repo.delete_task(user_id, task_id)
