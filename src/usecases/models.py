import uuid
from enum import Enum
from dataclasses import dataclass


class Status(str, Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"


@dataclass
class Task:
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    description: str | None
    status: Status = Status.created


@dataclass
class User:
    id: uuid.UUID
    username: str
