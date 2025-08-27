import pytest

from src.usecases.user_service import UserService


@pytest.mark.asyncio
async def test_create_user(postgres_repo):
    use_case = UserService(postgres_repo)
    user = await use_case.create_user(username="test username")
    assert user.username == "test username"

    user_in_db = await postgres_repo.get_user(user.id)
    assert user_in_db.username == "test username"


@pytest.mark.asyncio
async def test_get_user(postgres_repo):
    use_case = UserService(postgres_repo)
    user = await use_case.create_user(username="test username")
    get_user_result = await use_case.get_user(user_id=user.id)

    assert get_user_result.username == "test username"


@pytest.mark.asyncio
async def test_list_users(postgres_repo):
    use_case = UserService(postgres_repo)
    await use_case.create_user(username="test username")
    list_users_result = await use_case.list_users()

    assert isinstance(list_users_result, list)
