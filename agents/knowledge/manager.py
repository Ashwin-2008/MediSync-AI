import json
import logging
from typing import Dict, Any, Optional
from agents.shared.memory.cache import get_redis_client

logger = logging.getLogger(__name__)

class KnowledgeManager:
    """Manages high-frequency medical knowledge with Redis caching."""
    
    def __init__(self, ttl_seconds: int = 86400): # 24h default cache
        self.redis = get_redis_client()
        self.ttl = ttl_seconds

    def _get_cache_key(self, domain: str, key: str) -> str:
        return f"knowledge:{domain}:{key}"

    def get_knowledge(self, domain: str, key: str) -> Optional[Dict[str, Any]]:
        if not self.redis:
            logger.warning("Redis unavailable. Skipping cache lookup.")
            return None
            
        cache_key = self._get_cache_key(domain, key)
        try:
            cached = self.redis.get(cache_key)
            if cached:
                logger.info(f"Knowledge cache HIT for {cache_key}")
                return json.loads(cached)
        except Exception as e:
            logger.error(f"Redis error getting {cache_key}: {e}")
            
        logger.info(f"Knowledge cache MISS for {cache_key}")
        return None

    def set_knowledge(self, domain: str, key: str, data: Dict[str, Any]) -> None:
        if not self.redis:
            return
            
        cache_key = self._get_cache_key(domain, key)
        try:
            self.redis.setex(cache_key, self.ttl, json.dumps(data))
            logger.info(f"Knowledge cached for {cache_key}")
        except Exception as e:
            logger.error(f"Redis error setting {cache_key}: {e}")

    def invalidate_domain(self, domain: str) -> None:
        """Clears cache for an entire domain if policies are updated."""
        if not self.redis:
            return
            
        pattern = f"knowledge:{domain}:*"
        try:
            keys = self.redis.keys(pattern)
            if keys:
                self.redis.delete(*keys)
                logger.info(f"Invalidated {len(keys)} keys for domain {domain}")
        except Exception as e:
            logger.error(f"Error invalidating domain {domain}: {e}")

    # ==========================
    # Semantic Prompt Caching
    # ==========================
    
    def _hash_prompt(self, prompt: str) -> str:
        import hashlib
        return hashlib.sha256(prompt.encode('utf-8')).hexdigest()

    def get_semantic_cache(self, prompt: str) -> Optional[str]:
        if not self.redis: return None
        
        prompt_hash = self._hash_prompt(prompt)
        cache_key = f"semantic_cache:{prompt_hash}"
        try:
            cached = self.redis.get(cache_key)
            if cached:
                logger.info("Semantic Cache HIT - Bypassing LLM")
                return cached
        except Exception as e:
            logger.error(f"Redis semantic cache error: {e}")
        return None

    def set_semantic_cache(self, prompt: str, response: str) -> None:
        if not self.redis: return
        
        prompt_hash = self._hash_prompt(prompt)
        cache_key = f"semantic_cache:{prompt_hash}"
        try:
            self.redis.setex(cache_key, self.ttl, response)
        except Exception as e:
            logger.error(f"Redis semantic cache error: {e}")

knowledge_manager = KnowledgeManager()
