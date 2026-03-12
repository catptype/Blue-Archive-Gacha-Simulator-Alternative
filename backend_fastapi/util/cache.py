import fnmatch
import json
import redis
import logging
from ..config import settings
from abc import ABC, abstractmethod

CACHE_TYPE = settings.CACHE_TYPE.lower() # redis or memory
LOGGER = logging.getLogger(__name__)
REDIS_URL = settings.REDIS_URL

class Cache(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value, expire: int):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def delete_by_pattern(self, pattern: str):
        pass

class InMemoryCache(Cache):
    def __init__(self):
        self._cache = {}
        LOGGER.debug("✅ Using In-Memory Cache (for development)")

    def get(self, key: str):
        value = self._cache.get(key)
        if value: return json.loads(value)
        return None

    def set(self, key: str, value, expire: int = 300):
        self._cache[key] = json.dumps(value, default=str)

    def delete(self, key: str):
        if key in self._cache: del self._cache[key]
    
    def delete_by_pattern(self, pattern: str):
        keys_to_delete = [k for k in self._cache if fnmatch.fnmatch(k, pattern)]
        LOGGER.debug(f"In-Memory Cache: Deleting {len(keys_to_delete)} keys matching '{pattern}'")
        for key in keys_to_delete:
            del self._cache[key]

class RedisCache(Cache):
    def __init__(self):
        self.redis_client = redis.from_url(
            REDIS_URL,
            decode_responses=True # Decode from bytes to string
        )
        LOGGER.debug("🚀 Using Redis Cache (for production)")

    def get(self, key: str):
        value = self.redis_client.get(key)
        if value: return json.loads(value)
        return None

    def set(self, key: str, value, expire: int = 300):
        self.redis_client.set(key, json.dumps(value, default=str), ex=expire)
        
    def delete(self, key: str):
        self.redis_client.delete(key)
    
    def delete_by_pattern(self, pattern: str):
        keys_to_delete = [key for key in self.redis_client.scan_iter(match=pattern)]
        if keys_to_delete:
            LOGGER.debug(f"Redis Cache: Deleting {len(keys_to_delete)} keys matching '{pattern}'")
            self.redis_client.delete(*keys_to_delete)

def get_cache_client() -> Cache:
    """
    Factory function to decide which cache implementation to use
    based on the CACHE_TYPE environment variable.
    """
    if CACHE_TYPE == "redis":
        return RedisCache()
    return InMemoryCache()

# Create a single instance that will be shared across the application
cache_client: Cache = get_cache_client()

# This is the dependency that our endpoints will use
def get_cache() -> Cache:
    return cache_client