from typing import Annotated

from fastapi import Depends

from src.api.deps.repos import MemberRepoDep, ProjectRepoDep
from src.schemas.project import ProjectFilterParams
from src.services.project import ProjectService


def get_project_service(
    project_repo: ProjectRepoDep,
    member_repo: MemberRepoDep
) -> ProjectService:
    return ProjectService(project_repo, member_repo)


ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]
ProjectFiltersDep = Annotated[ProjectFilterParams, Depends()]
