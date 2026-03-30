from sqlalchemy import select, or_

from .base import BaseRepository
from src.models.user import User


class UserRepository(BaseRepository[User]):
    """
    User repository class
    """

    model = User

    async def get_by_username(self, username: str) -> User | None:
        return await self.session.scalar(
            select(User).where(User.username == username)
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
