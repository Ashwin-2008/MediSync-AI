import time
import logging
import os
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Provider(Enum):
    GEMINI = "gemini"
    GROQ   = "groq"   # used for OpenRouter


class APIKey:
    def __init__(self, key: str, provider: Provider):
        self.key            = key
        self.provider       = provider
        self.usage_count    = 0
        self.cooldown_until = 0.0

    @property
    def is_in_cooldown(self) -> bool:
        return time.time() < self.cooldown_until

    def add_cooldown(self, seconds: int):
        self.cooldown_until = time.time() + seconds
        logger.warning("[APIManager] key=***%s provider=%s cooldown=%ds",
                       self.key[-4:], self.provider.value, seconds)


class APIManager:
    def __init__(self):
        self.keys: Dict[Provider, List[APIKey]] = {
            Provider.GEMINI: [],
            Provider.GROQ:   [],
        }
        self._loaded = False

    def _load(self):
        """Load (or reload) keys from .env. Safe to call multiple times."""
        load_dotenv(_ENV_FILE, override=True)

        # Preserve existing cooldown state by key string
        existing: Dict[str, APIKey] = {}
        for key_list in self.keys.values():
            for k in key_list:
                existing[k.key] = k

        self.keys = {Provider.GEMINI: [], Provider.GROQ: []}

        for i in range(1, 5):
            raw = os.getenv(f"GEMINI_KEY_{i}", "").strip()
            if raw:
                obj = existing.get(raw) or APIKey(raw, Provider.GEMINI)
                self.keys[Provider.GEMINI].append(obj)

        raw_or = os.getenv("OPENROUTER_KEY", "").strip()
        if raw_or:
            obj = existing.get(raw_or) or APIKey(raw_or, Provider.GROQ)
            self.keys[Provider.GROQ].append(obj)

        logger.info(
            "[APIManager] loaded %d Gemini key(s), %d OpenRouter key(s)",
            len(self.keys[Provider.GEMINI]),
            len(self.keys[Provider.GROQ]),
        )
        self._loaded = True

    def reload(self):
        """Force re-read of .env — call after updating keys without restarting."""
        self._load()

    def get_key(self, provider: Provider) -> Optional[str]:
        if not self._loaded:
            self._load()

        available = [k for k in self.keys[provider] if not k.is_in_cooldown]
        if not available:
            # Try reloading in case new keys were added to .env
            self._load()
            available = [k for k in self.keys[provider] if not k.is_in_cooldown]

        if not available:
            logger.warning("[APIManager] No available keys for provider=%s", provider.value)
            return None

        available.sort(key=lambda k: k.usage_count)
        best = available[0]
        best.usage_count += 1
        return best.key

    def report_error(self, key_str: str, status_code: int):
        for key_list in self.keys.values():
            for k in key_list:
                if k.key == key_str:
                    if status_code == 429:
                        # Daily quota exhaustion — cool down for 1 hour
                        # (per-minute quota resets in 60s, daily resets at midnight)
                        k.add_cooldown(3600)
                    elif status_code in (408, 500, 502, 503, 504):
                        k.add_cooldown(60)
                    return


api_manager = APIManager()
