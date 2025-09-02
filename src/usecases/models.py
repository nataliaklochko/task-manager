from enum import Enum
from dataclasses import dataclass


class Status(str, Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"


@dataclass
class Task:
    user_id: int
    title: str
    description: str | None
    id: int | None = None
    status: Status = Status.created


@dataclass
class User:
    username: str
    id: int | None = None
