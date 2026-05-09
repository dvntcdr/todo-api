from sqlalchemy import func, or_, select

from src.models.user import User
from src.repos.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository class
    """

    model = User

    async def get_by_username(self, username: str) -> User | None:
        return await self.session.scalar(
            select(User).where(User.username == username)
        )

    async def get_by_email(self, email: str) -> User | None:
        return await self.session.scalar(
            select(User).where(User.email == email)
        )

    async def get_by_username_or_email(self, username: str = '', email: str = '') -> User | None:
        return await self.session.scalar(
            select(User).where(
                or_(
                    User.username == username,
                    User.email == email
                )
            )
        )

    async def get_all(self) -> tuple[list[User], int]:  # type: ignore
        stmt = select(User)

        total = await self.session.scalar(
            select(func.count()).select_from(User)
        ) or 0
        result = await self.session.scalars(stmt)

        return list(result), total

    async def search(self, query: str, limit: int = 10) -> list[User]:
        tsquery = func.websearch_to_tsquery('english', query)

        stmt = (
            select(User)
            .where(
                User.search_vector.op('@@')(tsquery),
                User.is_active,
                User.is_verified
            )
            .order_by(func.ts_rank(User.search_vector, tsquery).desc())
            .limit(limit)
        )

        return list(await self.session.scalars(stmt))
