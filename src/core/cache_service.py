import json
from uuid import UUID

from redis.asyncio import Redis


class CacheService:
    """
    Redis cache service class
    """

    USER_TTL: int = 300
    MEMBERSHIP_TTL: int = 300

    def __init__(self, redis_client: Redis) -> None:
        self.client = redis_client

    # USER

    def _user_key(self, username: str) -> str:
        return f'user:username:{username}'

    async def get_user(self, username: str) -> dict | None:
        data = await self.client.get(self._user_key(username))
        return json.loads(data) if data else None

    async def set_user(self, username: str, data: dict) -> None:
        await self.client.setex(
            self._user_key(username),
            self.USER_TTL,
            json.dumps(data)
        )

    async def invalidate_user(self, username: str) -> None:
        await self.client.delete(self._user_key(username))

    # MEMBERSHIP

    def _membership_key(self, project_id: UUID, user_id: UUID) -> str:
        return f'membership:{str(project_id)}:{str(user_id)}'

    async def get_membership(self, project_id: UUID, user_id: UUID) -> dict | None:
        data = await self.client.get(self._membership_key(project_id, user_id))
        return json.loads(data) if data else None

    async def set_membership(self, project_id: UUID, user_id: UUID, data: dict) -> None:
        await self.client.setex(
            self._membership_key(project_id, user_id),
            self.MEMBERSHIP_TTL,
            json.dumps(data)
        )

    async def invalidate_membership(self, project_id: UUID, user_id: UUID) -> None:
        await self.client.delete(self._membership_key(project_id, user_id))
