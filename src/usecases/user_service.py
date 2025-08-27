import uuid

from src.usecases.models import User
from src.interfaces.repository import IRepository


class UserService:
    def __init__(self, repo: IRepository):
        self.repo = repo

    async def create_user(self, username: str) -> User:
        user = User(id=uuid.uuid4(), username=username)
        return await self.repo.create_user(user)

    async def get_user(self, user_id: uuid.UUID) -> User | None:
        return await self.repo.get_user(user_id)

    async def list_users(self) -> list[User]:
        return await self.repo.list_users()
