from fastapi import APIRouter
from src.schemas.project_member import MemberResponse
from src.api.deps.project_member import MemberServiceDep
from uuid import UUID
from src.models.project_member import ProjectMember
from src.api.deps.auth import CurrentUserDep


router = APIRouter(prefix='/projects/{project_id}/members', tags=['project members'])


@router.get('/', response_model=list[MemberResponse])
async def get_members(
    project_id: UUID,
    service: MemberServiceDep,
    current_user: CurrentUserDep
) -> list[ProjectMember]:
    return await service.get_members(project_id, current_user)
