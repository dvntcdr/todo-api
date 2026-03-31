from uuid import UUID

from sqlalchemy import select

from .base import BaseRepository
from src.models.project import Project


class ProjectRepository(BaseRepository[Project]):
    """
    Project repository class
    """

    model = Project

    async def get_all_by_owner(self, user_id: UUID) -> list[Project]:
        result = await self.session.scalars(
            select(Project).where(Project.owner_id == user_id)
        )
        return list(result.all())
