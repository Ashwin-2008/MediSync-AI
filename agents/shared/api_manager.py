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
        from dotenv import load_dotenv
        load_dotenv()
        for i in range(1, 5):
            gemini_key = os.getenv(f"GEMINI_KEY_{i}")
            if gemini_key and gemini_key.strip():
                self.keys[Provider.GEMINI].append(APIKey(gemini_key, Provider.GEMINI))
            
        or_key = os.getenv("OPENROUTER_KEY")
        if or_key and or_key.strip():
            self.keys[Provider.GROQ].append(APIKey(or_key, Provider.GROQ))

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
        """Gets the best available key for the provider."""
        key_obj = self._get_best_key(provider)
        
        if key_obj:
            return key_obj.key
            
        logger.warning(f"All keys for {provider.value} are exhausted or in cooldown.")
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
