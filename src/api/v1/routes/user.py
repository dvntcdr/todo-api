from uuid import UUID

from fastapi import APIRouter, status

from src.api.deps.auth import CurrentUserDep
from src.api.deps.domain.user import UserServiceDep
from src.api.deps.pagination import PaginationDep
from src.models.user import User
from src.schemas.pagination import PagedResponse
from src.schemas.user import (
    ChangeEmailRequest,
    ChangeUsernameRequest,
    ConfirmEmailChangeRequest,
    UserResponse,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=PagedResponse[UserResponse])
async def get_users(
    service: UserServiceDep,
    current_user: CurrentUserDep,
    pg_params: PaginationDep
) -> PagedResponse[UserResponse]:
    return await service.get_all(pg_params)


@router.get('/{user_id}', response_model=UserResponse)
async def get_user(
    service: UserServiceDep,
    current_user: CurrentUserDep,
    user_id: UUID
) -> User:
    return await service.get_by_id(user_id)


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
) -> User:
    return await service.change_username(current_user, data)


@router.patch('/change-email', status_code=status.HTTP_204_NO_CONTENT)
async def change_email(
    service: UserServiceDep,
    current_user: CurrentUserDep,
    data: ChangeEmailRequest
) -> None:
    return await service.initiate_change_email(current_user, data)


@router.post('/confirm-email-change', response_model=UserResponse)
async def confirm_email_change(
    service: UserServiceDep,
    current_user: CurrentUserDep,
    data: ConfirmEmailChangeRequest
) -> User:
    return await service.confirm_email_change(current_user, data.token)
