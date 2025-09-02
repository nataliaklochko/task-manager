import pytest

from src.external.models import Task as TaskORM, User as UserORM
from src.usecases.models import Status


@pytest.mark.asyncio
async def test_create_and_get_task(postgres_repo, user):
    task = TaskORM(
        title="Test task",
        description="desc",
        status=Status.created,
        user_id=user.id,
    )
    created = await postgres_repo.create_task(task)
    assert created.id is not None
    assert created.title == "Test task"

    fetched = await postgres_repo.get_task(user_id=user.id, task_id=created.id)
    assert fetched is not None
    assert fetched.title == "Test task"


@pytest.mark.asyncio
async def test_list_tasks(postgres_repo, user):
    task1 = TaskORM(
        title="Task1",
        description=None,
        status=Status.created,
        user_id=user.id,
    )
    task2 = TaskORM(
        title="Task2",
        description=None,
        status=Status.in_progress,
        user_id=user.id,
    )

    await postgres_repo.create_task(task1)
    await postgres_repo.create_task(task2)

    tasks = await postgres_repo.list_tasks(user_id=user.id)
    assert isinstance(tasks, list)


@pytest.mark.asyncio
async def test_update_task(postgres_repo, user):
    task = TaskORM(
        title="Old title",
        description="old",
        status=Status.created,
        user_id=user.id,
    )
    created = await postgres_repo.create_task(task)

    created.title = "New title"
    created.status = Status.completed
    updated = await postgres_repo.update_task(task=created, user_id=user.id)

    assert updated.title == "New title"
    assert updated.status == Status.completed


@pytest.mark.asyncio
async def test_delete_task(postgres_repo, user):
    task = TaskORM(
        title="Delete me",
        description=None,
        status=Status.created,
        user_id=user.id,
    )
    created = await postgres_repo.create_task(task)

    result = await postgres_repo.delete_task(user_id=user.id, task_id=created.id)
    assert result is True

    missing = await postgres_repo.get_task(user_id=user.id, task_id=created.id)
    assert missing is None


@pytest.mark.asyncio
async def test_create_and_get_user(postgres_repo):
    user = UserORM(username="Test username")
    created = await postgres_repo.create_user(user)
    assert created.id is not None
    assert created.username == "Test username"

    fetched = await postgres_repo.get_user(user_id=created.id)
    assert fetched is not None
    assert fetched.username == "Test username"


@pytest.mark.asyncio
async def test_list_users(postgres_repo):
    user1 = UserORM(username="Test username 1")
    user2 = UserORM(username="Test username 2")

    await postgres_repo.create_user(user1)
    await postgres_repo.create_user(user2)

    users = await postgres_repo.list_users()
    assert isinstance(users, list)
