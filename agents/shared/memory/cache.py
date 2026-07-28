import json
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

class MemoryCache:
    def __init__(self):
        self.store = {}

    def get(self, key: str) -> Optional[Any]:
        val = self.store.get(key)
        if val:
            try:
                return json.loads(val)
            except:
                return val
        return None

    def set(self, key: str, value: Any, ex: int = 3600):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.store[key] = value

    def delete(self, key: str):
        if key in self.store:
            del self.store[key]

cache = MemoryCache()

def get_cache_client():
    return cache
