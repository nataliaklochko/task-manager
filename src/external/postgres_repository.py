from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.usecases.models import Task, User
from src.interfaces.repository import IRepository
from src.external.models import Task as TaskORM, User as UserORM


class PostgresRepository(IRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task: Task) -> Task:
        orm_task = TaskORM(
            title=task.title,
            description=task.description,
            status=task.status,
            user_id=task.user_id,
        )
        self.session.add(orm_task)
        await self.session.commit()
        return Task(
            user_id=orm_task.id,
            title=orm_task.title,
            description=orm_task.description,
            id=orm_task.id,
            status=orm_task.status,
        )

    async def get_task(self, user_id: int, task_id: int) -> Task | None:
        result = await self.session.execute(
            select(TaskORM).where(TaskORM.id == task_id, TaskORM.user_id == user_id)
        )
        orm_task = result.scalars().first()
        if orm_task:
            return Task(
                id=orm_task.id,
                title=orm_task.title,
                description=orm_task.description,
                status=orm_task.status,
                user_id=orm_task.user_id,
            )
        return None

    async def list_tasks(self, user_id: int) -> list[Task]:
        result = await self.session.execute(
            select(TaskORM).where(TaskORM.user_id == user_id)
        )
        return [
            Task(
                id=t.id,
                title=t.title,
                description=t.description,
                status=t.status,
                user_id=t.user_id,
            )
            for t in result.scalars().all()
        ]

    async def update_task(self, user_id: int, task: Task) -> Task | None:
        result = await self.session.execute(
            select(TaskORM).where(TaskORM.id == task.id, TaskORM.user_id == user_id)
        )
        orm_task = result.scalars().first()
        if not orm_task:
            return None
        orm_task.title = task.title
        orm_task.description = task.description
        orm_task.status = task.status
        await self.session.commit()
        return Task(
            id=orm_task.id,
            title=orm_task.title,
            description=orm_task.description,
            status=orm_task.status,
            user_id=orm_task.user_id,
        )

    async def delete_task(self, user_id: int, task_id: int) -> bool:
        result = await self.session.execute(
            select(TaskORM).where(TaskORM.id == task_id, TaskORM.user_id == user_id)
        )
        orm_task = result.scalars().first()
        if orm_task:
            await self.session.delete(orm_task)
            await self.session.commit()
            return True
        return False

    async def create_user(self, user: User) -> User:
        orm_user = UserORM(id=user.id, username=user.username)
        self.session.add(orm_user)
        await self.session.commit()
        return User(
            username=orm_user.username,
            id=orm_user.id,
        )

    async def get_user(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.id == user_id)
        )
        orm_user = result.scalars().first()
        if orm_user:
            return User(id=orm_user.id, username=orm_user.username)
        return None

    async def list_users(self) -> list[User]:
        result = await self.session.execute(select(UserORM))
        return [User(id=u.id, username=u.username) for u in result.scalars().all()]
