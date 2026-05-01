import redis.asyncio as aioredis
from src.core.config import settings


redis_client: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis | None:
    """
    Return the current Redis client instance, or None if not connected.
    """
    return redis_client


async def connect_redis() -> None:
    """
    Initialize and connect the Redis client using the configured REDIS_URL.
    """
    global redis_client
    redis_client = aioredis.from_url(
        url=settings.REDIS_URL,
        encoding='utf-8',
        decode_responses=True
    )


async def disconnect_redis() -> None:
    """
    Close the Redis client connection if it is currently active.
    """
    if redis_client is not None:
        await redis_client.aclose()
