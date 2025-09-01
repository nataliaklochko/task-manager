from fastapi import APIRouter, HTTPException, Depends
from dependency_injector.wiring import inject, Provide
from uuid import UUID

from src.app.models.users import CreateUserRequest, UserResponse
from src.usecases.user_service import UserService
from src.app.container import Container


router = APIRouter()


@router.post("/users/", response_model=UserResponse)
@inject
async def create_user(
    request: CreateUserRequest,
    service: UserService = Depends(Provide[Container.user_service]),
):
    user = await service.create_user(request.username)
    return UserResponse.from_entity(user)


@router.get("/users/{user_id}", response_model=UserResponse)
@inject
async def get_user(
    user_id: UUID,
    service: UserService = Depends(Provide[Container.user_service]),
):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return UserResponse.from_entity(user)


@router.get("/users/", response_model=list[UserResponse])
@inject
async def list_users(service: UserService = Depends(Provide[Container.user_service])):
    users = await service.list_users()
    return [UserResponse.from_entity(t) for t in users]
