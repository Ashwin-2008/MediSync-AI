import json
import logging
from typing import Dict, Any, Optional
from agents.shared.memory.cache import get_cache_client

logger = logging.getLogger(__name__)

class KnowledgeManager:
    """Manages high-frequency medical knowledge with in-memory caching."""
    
    def __init__(self, ttl_seconds: int = 86400):
        self.cache = get_cache_client()
        self.ttl = ttl_seconds

    def _get_cache_key(self, domain: str, key: str) -> str:
        return f"knowledge:{domain}:{key}"

    def get_knowledge(self, domain: str, key: str) -> Optional[Dict[str, Any]]:
        cache_key = self._get_cache_key(domain, key)
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Knowledge cache HIT for {cache_key}")
            return cached
            
        logger.info(f"Knowledge cache MISS for {cache_key}")
        return None

    def set_knowledge(self, domain: str, key: str, data: Dict[str, Any]) -> None:
        cache_key = self._get_cache_key(domain, key)
        self.cache.set(cache_key, data, ex=self.ttl)
        logger.info(f"Knowledge cached for {cache_key}")

    def invalidate_domain(self, domain: str) -> None:
        """Clears cache for an entire domain if policies are updated."""
        pattern = f"knowledge:{domain}:"
        keys_to_delete = [k for k in self.cache.store.keys() if k.startswith(pattern)]
        for k in keys_to_delete:
            self.cache.delete(k)
        if keys_to_delete:
            logger.info(f"Invalidated {len(keys_to_delete)} keys for domain {domain}")

    # ==========================
    # Semantic Prompt Caching
    # ==========================
    
    def _hash_prompt(self, prompt: str) -> str:
        import hashlib
        return hashlib.sha256(prompt.encode('utf-8')).hexdigest()

    def get_semantic_cache(self, prompt: str) -> Optional[str]:
        prompt_hash = self._hash_prompt(prompt)
        cache_key = f"semantic_cache:{prompt_hash}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info("Semantic Cache HIT - Bypassing LLM")
            return cached
        return None

    def set_semantic_cache(self, prompt: str, response: str) -> None:
        prompt_hash = self._hash_prompt(prompt)
        cache_key = f"semantic_cache:{prompt_hash}"
        self.cache.set(cache_key, response, ex=self.ttl)

knowledge_manager = KnowledgeManager()
