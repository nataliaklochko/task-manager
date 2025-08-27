from dependency_injector import containers, providers

from src.external.db import async_session_factory
from src.external.postgres_repository import PostgresRepository
from src.usecases.task_service import TaskService
from src.usecases.user_service import UserService


class Container(containers.DeclarativeContainer):
    cfg = providers.Configuration()

    db_session = providers.Resource(async_session_factory)
    repository = providers.Singleton(PostgresRepository, session=db_session)

    task_service = providers.Singleton(TaskService, repo=repository)
    user_service = providers.Singleton(UserService, repo=repository)
