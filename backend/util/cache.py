import os
import json
from abc import ABC, abstractmethod
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TYPE = os.getenv("CACHE_TYPE", "memory").lower() # redis or memory

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

class InMemoryCache(Cache):
    def __init__(self):
        self._cache = {}
        print("✅ Using In-Memory Cache (for development)")

    def get(self, key: str):
        value = self._cache.get(key)
        if value:
            # Pydantic models are not directly JSON serializable, so we store them as dicts.
            # In a real app, you'd serialize/deserialize properly.
            return json.loads(value)
        return None

    def set(self, key: str, value, expire: int = 300):
        # We convert the value (often a list of Pydantic models) to a JSON string
        self._cache[key] = json.dumps(value, default=str)

    def delete(self, key: str):
        if key in self._cache:
            del self._cache[key]

class RedisCache(Cache):
    def __init__(self):
        # Assumes Redis is running on localhost:6379.
        # Use REDIS_URL environment variable for production.
        self.redis_client = redis.from_url(
            REDIS_URL,
            decode_responses=True # Decode from bytes to string
        )
        print("🚀 Using Redis Cache (for production)")

    def get(self, key: str):
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value, expire: int = 300):
        # The 'default=str' is a safety net for things json can't serialize, like datetimes.
        self.redis_client.set(key, json.dumps(value, default=str), ex=expire)
        
    def delete(self, key: str):
        self.redis_client.delete(key)


# --- 4. The Factory and Dependency ---
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