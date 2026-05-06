from uuid import UUID

from fastapi import APIRouter, status
from fastapi.requests import Request

from src.api.deps.auth import CurrentUserDep
from src.api.deps.domain.task import TaskFiltersDep, TaskServiceDep
from src.api.deps.pagination import PaginationDep
from src.infra.rate_limit.limiter import limiter
from src.models.task import Task
from src.schemas.pagination import PagedResponse
from src.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get('/', response_model=PagedResponse[TaskResponse])
@limiter.limit('60/minute')
async def get_tasks(
    request: Request,
    service: TaskServiceDep,
    current_user: CurrentUserDep,
    pg_params: PaginationDep,
    filters: TaskFiltersDep
) -> PagedResponse[TaskResponse]:
    return await service.get_all(current_user, pg_params, filters)


@router.get('/{task_id}', response_model=TaskResponse)
@limiter.limit('100/minute')
async def get_task(
    request: Request,
    service: TaskServiceDep,
    task_id: UUID,
    current_user: CurrentUserDep
) -> Task:
    return await service.get_by_id(task_id, current_user)


@router.post('/', response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit('20/minute')
async def create_task(
    request: Request,
    service: TaskServiceDep,
    data: TaskCreate,
    current_user: CurrentUserDep
) -> Task:
    return await service.create(data, current_user)


@router.patch('/{task_id}', response_model=TaskResponse)
@limiter.limit('30/minute')
async def update_task(
    request: Request,
    service: TaskServiceDep,
    task_id: UUID,
    data: TaskUpdate,
    current_user: CurrentUserDep
):
    return await service.update(task_id, data, current_user)


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit('15/minute')
async def delete_task(
    request: Request,
    service: TaskServiceDep,
    task_id: UUID,
    current_user: CurrentUserDep
) -> None:
    return await service.delete(task_id, current_user)
