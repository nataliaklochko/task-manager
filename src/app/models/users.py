from pydantic import BaseModel

from src.usecases.models import User


class CreateUserRequest(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: int
    username: str

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            id=user.id,
            username=user.username,
        )
