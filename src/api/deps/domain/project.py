from typing import Annotated

from fastapi import Depends

from src.api.deps.cache import CacheServiceDep
from src.api.deps.db.repos import MemberRepoDep, ProjectRepoDep
from src.schemas.project import ProjectFilterParams
from src.services.project import ProjectService


def get_project_service(
    project_repo: ProjectRepoDep,
    member_repo: MemberRepoDep,
    cache: CacheServiceDep
) -> ProjectService:
    return ProjectService(project_repo, member_repo, cache)


ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]
ProjectFiltersDep = Annotated[ProjectFilterParams, Depends()]
