from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple


@dataclass
class CacheEntry:
    value: Any
    expiry: float


class InMemoryCache:
    """A very small in-memory cache with TTL support."""

    def __init__(self, default_ttl: int = 300) -> None:
        self._store: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl

    def _is_expired(self, entry: CacheEntry) -> bool:
        return entry.expiry < time.time()

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None
        if self._is_expired(entry):
            del self._store[key]
            return None
        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl = ttl if ttl is not None else self._default_ttl
        self._store[key] = CacheEntry(value=value, expiry=time.time() + ttl)

    def get_or_set(self, key: str, factory: Callable[[], Any], ttl: Optional[int] = None) -> Any:
        cached = self.get(key)
        if cached is not None:
            return cached
        value = factory()
        self.set(key, value, ttl)
        return value

    def invalidate(self, *keys: str) -> None:
        for key in keys:
            self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()


cache = InMemoryCache(default_ttl=120)
