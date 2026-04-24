from typing import Awaitable, Callable

from src.core.caching.cache_service import CacheService
from src.core.exceptions import NotFoundException


class CacheManager[M]:
    """
    Generic cache manager
    """
    
    def __init__(self, cache: CacheService, model_cls: type[M]) -> None:
        self.cache = cache
        self.model_cls = model_cls
    
    async def get_or_fetch(
        self,
        key: str,
        fetch: Callable[[], Awaitable[M | None]],
        use_cache: bool = True
    ) -> M:
        if use_cache:
            try:
                cached = await self.cache.get(key)
                if cached:
                    return self.model_cls.from_dict(cached)  # type: ignore
            except Exception:
                pass
        
        instance = await fetch()

        if instance is None:
            raise NotFoundException()
        
        if use_cache:
            try:
                await self.cache.set(key, instance.to_dict())  # type: ignore
            except Exception:
                pass
        
        return instance
    
    async def set(self, key: str, instance: M) -> None:
        try:
            await self.cache.set(key, instance.to_dict())  # type: ignore
        except Exception:
            pass

    async def invalidate(self, *keys: str) -> None:
        try:
            await self.cache.invalidate(*keys)
        except Exception:
            pass
