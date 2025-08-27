from fastapi import FastAPI

from src.app.routers.tasks import router as task_router
from src.app.routers.users import router as user_router
from src.app.container import Container


container = Container()


def create_app() -> FastAPI:
    app = FastAPI(title="Task Manager with DI")

    app.include_router(task_router)
    app.include_router(user_router)

    container.wire(modules=["src.app.routers.tasks", "src.app.routers.users"])

    return app
