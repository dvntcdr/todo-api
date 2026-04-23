from typing import Annotated

from fastapi import Depends

from src.api.deps.domain.user import UserRepoDep
from src.services.membership import ProjectMemberService
from src.api.deps.db.repos import MemberRepoDep, ProjectRepoDep


def get_member_service(
    member_repo: MemberRepoDep,
    project_repo: ProjectRepoDep,
    user_repo: UserRepoDep
) -> ProjectMemberService:
    return ProjectMemberService(member_repo, project_repo, user_repo)


MemberServiceDep = Annotated[ProjectMemberService, Depends(get_member_service)]
