from typing import Annotated

from fastapi import Depends

from src.api.deps.domain.project import ProjectRepoDep
from src.api.deps.domain.task import TaskRepoDep
from src.services.search import SearchService
from src.schemas.search import SearchRequest
from src.api.deps.domain.user import UserRepoDep


def get_search_service(
    task_repo: TaskRepoDep,
    project_repo: ProjectRepoDep,
    user_repo: UserRepoDep
) -> SearchService:
    return SearchService(task_repo, project_repo, user_repo)


SearchServiceDep = Annotated[SearchService, Depends(get_search_service)]

SearchParamsDep = Annotated[SearchRequest, Depends()]
