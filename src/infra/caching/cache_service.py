import json

from redis.asyncio import Redis


class CacheService:
    """
    A service class for caching data using Redis.

    Attributes:
        DEFAULT_TTL (int): The default time-to-live in seconds for cached entries (300 seconds).
        client (Redis): The async Redis client used to interact with the Redis instance.
    """

    DEFAULT_TTL: int = 300

    def __init__(self, redis_client: Redis) -> None:
        self.client = redis_client

    async def set(self, key: str, data: dict, ttl: int | None = None) -> None:
        await self.client.setex(
            name=key,
            time=ttl or self.DEFAULT_TTL,
            value=json.dumps(data)
        )

    async def get(self, key: str) -> dict | None:
        data = await self.client.get(key)
        return json.loads(data) if data else None

    async def invalidate(self, *keys: str) -> None:
        await self.client.delete(*keys)
