from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.routers.tasks import router as task_router
from src.app.routers.users import router as user_router
from src.app.container import Container
from src.external.db import engine, Base


container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Task Manager with DI", lifespan=lifespan)

    app.include_router(task_router)
    app.include_router(user_router)

    container.wire(modules=["src.app.routers.tasks", "src.app.routers.users"])

    return app
