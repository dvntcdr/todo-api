from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from src.infra.caching.cache import get_redis
from src.infra.caching.cache_service import CacheService

RedisDep = Annotated[Redis, Depends(get_redis)]


def get_cache_service(redis_client: RedisDep) -> CacheService:
    return CacheService(redis_client)


CacheServiceDep = Annotated[CacheService, Depends(get_cache_service)]
