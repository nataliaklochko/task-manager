import pytest
from fastapi.testclient import TestClient
from dependency_injector import providers

from src.app.main import create_app, container
from src.external.postgres_repository import PostgresRepository


@pytest.fixture
def client(async_session):
    app = create_app()
    container.repository.override(
        providers.Singleton(PostgresRepository, session=async_session)
    )
    return TestClient(app)


@pytest.fixture
def user_id(client):
    response = client.post("/users/", json={"username": "Test username"})
    print(response.json())
    return response.json()["id"]


@pytest.fixture
def task_id(client, user_id):
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "desc", "user_id": user_id},
    )
    return response.json()["id"]
