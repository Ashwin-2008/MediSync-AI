import time
import logging
from enum import Enum
from typing import List, Dict, Optional
import os

logger = logging.getLogger(__name__)

class Provider(Enum):
    GEMINI = "gemini"
    GROQ = "groq"

class APIKey:
    def __init__(self, key: str, provider: Provider, priority: int = 0):
        self.key = key
        self.provider = provider
        self.priority = priority
        self.usage_count = 0
        self.cooldown_until = 0.0

    @property
    def is_in_cooldown(self) -> bool:
        return time.time() < self.cooldown_until

    def add_cooldown(self, seconds: int = 300):
        self.cooldown_until = time.time() + seconds
        logger.warning(f"Key for {self.provider.value} put in cooldown for {seconds}s")

class APIManager:
    def __init__(self):
        self.keys: Dict[Provider, List[APIKey]] = {
            Provider.GEMINI: [],
            Provider.GROQ: []
        }
        self.load_keys()

    def load_keys(self):
        # Load up to 4 keys per provider from environment variables
        for i in range(1, 5):
            gemini_key = os.getenv(f"GEMINI_KEY_{i}")
            if gemini_key:
                self.keys[Provider.GEMINI].append(APIKey(gemini_key, Provider.GEMINI))
            
            groq_key = os.getenv(f"GROQ_KEY_{i}")
            if groq_key:
                self.keys[Provider.GROQ].append(APIKey(groq_key, Provider.GROQ))

    def _get_best_key(self, provider: Provider) -> Optional[APIKey]:
        available_keys = [k for k in self.keys[provider] if not k.is_in_cooldown]
        if not available_keys:
            return None

        # Sort by: 1. Priority (desc), 2. Usage Count (asc)
        available_keys.sort(key=lambda k: (-k.priority, k.usage_count))
        
        best_key = available_keys[0]
        best_key.usage_count += 1
        return best_key

    def get_key(self, provider: Provider) -> Optional[str]:
        """Gets the best available key for the provider, falling back to the other provider if needed."""
        key_obj = self._get_best_key(provider)
        
        if key_obj:
            return key_obj.key
            
        # Fallback to the other provider if all keys are exhausted
        logger.warning(f"All keys for {provider.value} are exhausted or in cooldown. Attempting fallback.")
        fallback_provider = Provider.GROQ if provider == Provider.GEMINI else Provider.GEMINI
        fallback_key_obj = self._get_best_key(fallback_provider)
        
        if fallback_key_obj:
            logger.info(f"Successfully fell back to {fallback_provider.value}")
            return fallback_key_obj.key
            
        logger.error("All keys for both providers are exhausted or in cooldown.")
        return None

    def report_error(self, key_str: str, status_code: int):
        """Reports an error for a key. Puts in cooldown on 429."""
        for provider_keys in self.keys.values():
            for k in provider_keys:
                if k.key == key_str:
                    if status_code == 429:
                        k.add_cooldown(300) # 5 minutes cooldown
                    elif status_code in [408, 500, 502, 503, 504]:
                        k.add_cooldown(60) # 1 minute cooldown for temporary network issues
                    return

# Global singleton
api_manager = APIManager()
