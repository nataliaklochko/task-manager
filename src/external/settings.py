from pydantic_settings import BaseSettings


class PostgresDBSettings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/task_manager"
