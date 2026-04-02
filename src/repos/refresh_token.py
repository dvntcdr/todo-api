from uuid import UUID

from sqlalchemy import select

from src.models.refresh_token import RefreshToken
from src.repos.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """
    Refresh token repository class
    """

    model = RefreshToken

    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        return await self.session.scalar(
            select(RefreshToken).where(RefreshToken.hashed_token == token_hash)
        )

    async def revoke(self, instance: RefreshToken) -> None:
        instance.is_revoked = True
        await self.session.commit()

    async def revoke_all_for_user(self, user_id: UUID) -> None:
        tokens = await self.session.scalars(
            select(RefreshToken).where(RefreshToken.owner_id == user_id)
        )

        for token in tokens.all():
            token.is_revoked = True

        await self.session.commit()
