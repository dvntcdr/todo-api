from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[T]:
    """
    Base repository class with common methods
    """

    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        if not hasattr(self, 'model'):
            raise NotImplementedError('Subclasses must define "model"')
        self.session = session

    async def get_all(self) -> list[T]:
        return list(await self.session.scalars(select(self.model)))

    async def get_paginated(self, stmt: Select, offset: int, limit: int) -> tuple[list[T], int]:
        total = await self.session.scalar(
            select(func.count()).select_from(stmt.subquery())
        ) or 0
        result = await self.session.scalars(stmt.offset(offset).limit(limit))
        return list(result.all()), total

    async def get_by_id(self, id: UUID) -> T | None:
        return await self.session.get(self.model, id)

    async def create(self, instance: T) -> T:
        self.session.add(instance)

        await self.session.commit()
        await self.session.refresh(instance)

        return instance

    async def update(self, instance: T, data: dict) -> T:
        for field, value in data.items():
            setattr(instance, field, value)

        await self.session.commit()
        await self.session.refresh(instance)

        return instance

    async def delete(self, instance: T) -> None:
        await self.session.delete(instance)
        await self.session.commit()
