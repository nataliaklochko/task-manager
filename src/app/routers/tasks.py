from fastapi import APIRouter, HTTPException, Depends
from dependency_injector.wiring import inject, Provide
from uuid import UUID

from src.app.models.tasks import (
    CreateTaskRequest,
    UpdateTaskRequest,
    TaskResponse,
)
from src.usecases.task_service import TaskService
from src.app.container import Container


router = APIRouter()


@router.post("/tasks/", response_model=TaskResponse)
@inject
async def create_task(
    request: CreateTaskRequest,
    service: TaskService = Depends(Provide[Container.task_service]),
):
    task = await service.create_task(
        request.user_id, request.title, request.description
    )
    return TaskResponse.from_entity(task)


@router.get("/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
@inject
async def get_task(
    task_id: UUID,
    user_id: UUID,
    service: TaskService = Depends(Provide[Container.task_service]),
):
    task = await service.get_task(user_id=user_id, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_entity(task)


@router.get("/users/{user_id}/tasks/", response_model=list[TaskResponse])
@inject
async def list_tasks(
    user_id: UUID,
    service: TaskService = Depends(Provide[Container.task_service]),
):
    tasks = await service.list_tasks(user_id)
    return [TaskResponse.from_entity(t) for t in tasks]


@router.put("/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
@inject
async def update_task(
    task_id: UUID,
    user_id: UUID,
    request: UpdateTaskRequest,
    service: TaskService = Depends(Provide[Container.task_service]),
):
    task = await service.update_task(
        user_id,
        task_id,
        title=request.title,
        description=request.description,
        status=request.status,
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_entity(task)


@router.delete("/users/{user_id}/tasks/{task_id}")
@inject
async def delete_task(
    task_id: UUID,
    user_id: UUID,
    service: TaskService = Depends(Provide[Container.task_service]),
):
    success = await service.delete_task(user_id, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
