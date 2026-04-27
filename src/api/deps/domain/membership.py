from typing import Annotated

from fastapi import Depends

from src.api.deps.domain.user import UserRepoDep
from src.services.membership import ProjectMemberService
from src.api.deps.db.repos import MemberRepoDep, ProjectRepoDep
from src.api.deps.cache import CacheServiceDep


def get_member_service(
    member_repo: MemberRepoDep,
    project_repo: ProjectRepoDep,
    user_repo: UserRepoDep,
    cache: CacheServiceDep
) -> ProjectMemberService:
    return ProjectMemberService(member_repo, project_repo, user_repo, cache)


MemberServiceDep = Annotated[ProjectMemberService, Depends(get_member_service)]
