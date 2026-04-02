from uuid import UUID

from src.repos.project import ProjectRepository
from src.models.user import User
from src.models.project import Project
from src.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from src.schemas.pagination import PaginationParams, PagedResponse
from src.core.exceptions import (
    NotFoundException,
    ForbiddenException
)


class ProjectService:
    """
    Project service class
    """

    def __init__(self, repo: ProjectRepository) -> None:
        self.repo = repo

    async def _get_project_for_user(self, project_id: UUID, user: User) -> Project:
        project = await self.repo.get_by_id(project_id)

        if project is None:
            raise NotFoundException('Project not found')

        if project.owner_id != user.id:
            raise ForbiddenException()

        return project

    async def get_all(self, user: User, pg_params: PaginationParams) -> PagedResponse[ProjectResponse]:
        items, total = await self.repo.get_all_by_owner(user.id, pg_params.offset, pg_params.limit)
        return PagedResponse.create(items, total, pg_params)

    async def get_by_id(self, project_id: UUID, user: User) -> Project:
        return await self._get_project_for_user(project_id, user)

    async def create(self, data: ProjectCreate, user: User) -> Project:
        project = Project(**data.model_dump(exclude_unset=True), owner_id=user.id)
        return await self.repo.create(project)

    async def update(self, project_id: UUID, data: ProjectUpdate, user: User) -> Project:
        project = await self._get_project_for_user(project_id, user)
        return await self.repo.update(project, data.model_dump(exclude_unset=True))

    async def delete(self, project_id: UUID, user: User) -> None:
        project = await self._get_project_for_user(project_id, user)
        return await self.repo.delete(project)
