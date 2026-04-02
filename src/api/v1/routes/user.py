from fastapi import APIRouter

from src.api.deps.user import UserServiceDep
from src.api.deps.auth import CurrentUserDep
from src.models.user import User
from src.schemas.user import (
    UserResponse,
    ChangeUsernameRequest
)


router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me', response_model=UserResponse)
async def get_user_me(
    service: UserServiceDep,
    current_user: CurrentUserDep
) -> User:
    return await service.get_by_id(current_user.id)


@router.patch('/change-username', response_model=UserResponse)
async def change_username(
    service: UserServiceDep,
    current_user: CurrentUserDep,
    data: ChangeUsernameRequest
):
    return await service.change_username(current_user, data)
