from pydantic import BaseModel
from uuid import UUID

from src.usecases.models import User


class CreateUserRequest(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: UUID
    username: str

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            id=user.id,
            username=user.username,
        )
