from typing import Annotated

from fastapi import Depends

from src.api.deps.cache import CacheServiceDep
from src.api.deps.db.repos import MemberRepoDep, ProjectRepoDep, TaskRepoDep
from src.schemas.task import TaskFilterParams
from src.services.task import TaskService


def get_task_service(
    task_repo: TaskRepoDep,
    project_repo: ProjectRepoDep,
    member_repo: MemberRepoDep,
    cache: CacheServiceDep
) -> TaskService:
    return TaskService(task_repo, project_repo, member_repo, cache)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
TaskFiltersDep = Annotated[TaskFilterParams, Depends()]
