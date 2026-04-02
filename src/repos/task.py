from uuid import UUID

from sqlalchemy import select

from src.models.task import Task
from src.repos.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """
    Task repository class
    """

    model = Task

    async def get_all_by_owner(self, user_id: UUID, offset: int, limit: int):
        stmt = select(Task).where(Task.owner_id == user_id)
        return await self.get_paginated(stmt, offset, limit)
