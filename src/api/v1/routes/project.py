from uuid import UUID

from fastapi import APIRouter, status
from fastapi.requests import Request

from src.api.deps.auth import CurrentUserDep
from src.api.deps.domain.project import ProjectFiltersDep, ProjectServiceDep
from src.api.deps.pagination import PaginationDep
from src.infra.rate_limit.limiter import limiter
from src.models.project import Project
from src.schemas.pagination import PagedResponse
from src.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter(prefix='/projects', tags=['projects'])


@router.get('/', response_model=PagedResponse[ProjectResponse])
@limiter.limit('60/minute')
async def get_projects(
    request: Request,
    service: ProjectServiceDep,
    current_user: CurrentUserDep,
    pg_params: PaginationDep,
    filters: ProjectFiltersDep
) -> PagedResponse[ProjectResponse]:
    return await service.get_all(current_user, pg_params, filters)


@router.get('/{project_id}', response_model=ProjectResponse)
@limiter.limit('100/minute')
async def get_project(
    request: Request,
    service: ProjectServiceDep,
    project_id: UUID,
    current_user: CurrentUserDep
) -> Project:
    return await service.get_by_id(project_id, current_user)


@router.post('/', response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit('20/minute')
async def create_project(
    request: Request,
    service: ProjectServiceDep,
    data: ProjectCreate,
    current_user: CurrentUserDep
) -> Project:
    return await service.create(data, current_user)


@router.patch('/{project_id}', response_model=ProjectResponse)
@limiter.limit('30/minute')
async def update_project(
    request: Request,
    service: ProjectServiceDep,
    project_id: UUID,
    data: ProjectUpdate,
    current_user: CurrentUserDep
) -> Project:
    return await service.update(project_id, data, current_user)


@router.delete('/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit('15/minute')
async def delete_project(
    request: Request,
    service: ProjectServiceDep,
    project_id: UUID,
    current_user: CurrentUserDep
) -> None:
    return await service.delete(project_id, current_user)
