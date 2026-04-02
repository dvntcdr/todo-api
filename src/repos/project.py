from uuid import UUID

from sqlalchemy import select

from src.models.project import Project
from src.repos.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """
    Project repository class
    """

    model = Project

    async def get_all_by_owner(self, user_id: UUID, offset: int, limit: int) -> tuple[list[Project], int]:
        stmt = select(Project).where(Project.owner_id == user_id)
        return await self.get_paginated(stmt, offset, limit)
