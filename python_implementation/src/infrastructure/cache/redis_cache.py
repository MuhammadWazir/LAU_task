import json
import redis
from typing import Any, Optional, Union
import os
from src.domain.abstractions.cache.abstract_redis_cache import AbstractRedisCache

class RedisCache(AbstractRedisCache):
    def __init__(self, host: str, port: int, db: int = 0):
        self._redis = redis.Redis(
            host=host, 
            port=port, 
            db=db, 
            decode_responses=True
        )

    def get(self, key: str) -> Optional[Any]:
        value = self._redis.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    def set(self, key: str, value: Any, ttl: int = 10):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self._redis.setex(key, ttl, value)

    def delete(self, key: str):
        self._redis.delete(key)

    def invalidate_pattern(self, pattern: str):
        # Invalidate all keys matching a pattern (e.g., tasks:*)
        keys = self._redis.keys(pattern)
        if keys:
            self._redis.delete(*keys)

    def flush_all(self):
        self._redis.flushdb()
