from abc import ABC, abstractmethod
from typing import Any, Optional

class AbstractRedisCache(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 10):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def invalidate_pattern(self, pattern: str):
        pass

    @abstractmethod
    def flush_all(self):
        pass