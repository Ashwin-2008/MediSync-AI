import json
import logging
from typing import Any, Optional
# import redis

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        # self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.mock_store = {} # Using a dict for now until Redis container is spun up

    def get(self, key: str) -> Optional[Any]:
        # val = self.client.get(key)
        val = self.mock_store.get(key)
        if val:
            try:
                return json.loads(val)
            except:
                return val
        return None

    def set(self, key: str, value: Any, ex: int = 3600):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        # self.client.set(key, value, ex=ex)
        self.mock_store[key] = value

    def delete(self, key: str):
        # self.client.delete(key)
        if key in self.mock_store:
            del self.mock_store[key]

cache = RedisCache()
