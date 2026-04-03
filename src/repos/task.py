from typing import Any
from uuid import UUID

from sqlalchemy import Select, select, asc, desc

from src.models.task import Task
from src.repos.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """
    Task repository class
    """

    model = Task

    def _apply_filters(self, stmt: Select, filters: dict[str, Any]) -> Select:
        eq_filters = {
            'status': Task.status,
            'priority': Task.priority,
            'project_id': Task.project_id,
        }

        for field, column in eq_filters.items():
            if field in filters:
                stmt = stmt.where(column == filters[field])

        if 'due_date_from' in filters:
            stmt = stmt.where(Task.due_date >= filters['due_date_from'])
        if 'due_date_to' in filters:
            stmt = stmt.where(Task.due_date <= filters['due_date_to'])

        sort_by = filters.get('sort_by', 'created_at')
        sort_order = filters.get('sort_order', 'desc')
        sort_column = getattr(Task, sort_by)
        order_func = asc if sort_order == 'asc' else desc

        return stmt.order_by(order_func(sort_column))

    async def get_all_by_owner(
        self,
        user_id: UUID,
        offset: int,
        limit: int,
        filters: dict[str, Any] | None = None
    ) -> tuple[list[Task], int]:
        stmt = select(Task).where(Task.owner_id == user_id)

        if filters:
            stmt = self._apply_filters(stmt, filters)

        return await self.get_paginated(stmt, offset, limit)
