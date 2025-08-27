import pytest

from src.usecases.models import Status
from src.usecases.task_service import TaskService


@pytest.mark.asyncio
async def test_create_task(postgres_repo, user):
    use_case = TaskService(postgres_repo)
    task = await use_case.create_task(
        user_id=user.id, title="test title", description="test descr"
    )
    assert task.title == "test title"
    assert task.description == "test descr"

    task_in_db = await postgres_repo.get_task(user_id=user.id, task_id=task.id)
    assert task_in_db.title == "test title"
    assert task_in_db.description == "test descr"
    assert task_in_db.status == Status.created


@pytest.mark.asyncio
async def test_get_task(postgres_repo, user):
    use_case = TaskService(postgres_repo)
    task = await use_case.create_task(
        user_id=user.id, title="test title", description="test descr"
    )
    get_task_result = await use_case.get_task(user_id=user.id, task_id=task.id)

    assert get_task_result.title == "test title"
    assert get_task_result.description == "test descr"
    assert get_task_result.status == Status.created


@pytest.mark.asyncio
async def test_list_tasks(postgres_repo, user):
    use_case = TaskService(postgres_repo)
    await use_case.create_task(
        user_id=user.id, title="test title", description="test descr"
    )
    list_task_result = await use_case.list_tasks(user_id=user.id)

    assert isinstance(list_task_result, list)


@pytest.mark.asyncio
async def test_update_task(postgres_repo, user):
    use_case = TaskService(postgres_repo)
    task = await use_case.create_task(
        user_id=user.id, title="test title", description="test descr"
    )
    update_task_result = await use_case.update_task(
        user_id=user.id,
        task_id=task.id,
        status=Status.in_progress,
    )

    assert update_task_result.title == "test title"
    assert update_task_result.description == "test descr"
    assert update_task_result.status == Status.in_progress


@pytest.mark.asyncio
async def test_delete_task(postgres_repo, user):
    use_case = TaskService(postgres_repo)
    task = await use_case.create_task(
        user_id=user.id, title="test title", description="test descr"
    )

    assert await use_case.delete_task(user_id=user.id, task_id=task.id)
    task = await use_case.get_task(user_id=user.id, task_id=task.id)

    assert not task
