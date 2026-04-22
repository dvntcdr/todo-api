import redis.asyncio as aioredis
from src.core.config import settings


redis_client: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis | None:
    return redis_client


async def connect_redis() -> None:
    global redis_client
    redis_client = aioredis.from_url(
        url=settings.REDIS_URL,
        encoding='utf-8',
        decode_response=True
    )


async def disconnect_redis() -> None:
    if redis_client is not None:
        await redis_client.aclose()
