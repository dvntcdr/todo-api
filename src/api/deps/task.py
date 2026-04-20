from typing import Annotated

from fastapi import Depends

from src.api.deps.repos import ProjectRepoDep, TaskRepoDep, MemberRepoDep
from src.schemas.task import TaskFilterParams
from src.services.task import TaskService


def get_task_service(
    task_repo: TaskRepoDep,
    project_repo: ProjectRepoDep,
    member_repo: MemberRepoDep
) -> TaskService:
    return TaskService(task_repo, project_repo, member_repo)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
TaskFiltersDep = Annotated[TaskFilterParams, Depends()]
