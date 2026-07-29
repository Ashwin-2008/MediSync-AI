from pathlib import Path
from typing import Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve .env relative to this file's location so it works regardless of CWD.
# This file lives at:  <project_root>/backend/core/config.py
# .env lives at:       <project_root>/.env
_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hospital Multi-Agent AI Coordination Platform"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "local"

    SECRET_KEY: str = "hospital_super_secret_key_change_me_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    DATABASE_URL: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"

    # Matches the key name in .env exactly.
    # Accepts either a JSON array string: '["http://localhost:5173"]'
    # or a comma-separated string: "http://localhost:5173,http://localhost:3000"
    BACKEND_CORS_ORIGINS: Union[list[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, list]) -> list[str]:
        if isinstance(v, list):
            return v
        # JSON array format: '["http://localhost:5173","http://localhost:3000"]'
        if v.startswith("["):
            import json
            return json.loads(v)
        # Comma-separated format: "http://localhost:5173,http://localhost:3000"
        return [origin.strip() for origin in v.split(",") if origin.strip()]

    # AI Provider Keys
    GEMINI_KEY_1: Optional[str] = None
    GEMINI_KEY_2: Optional[str] = None
    GEMINI_KEY_3: Optional[str] = None
    GEMINI_KEY_4: Optional[str] = None
    OPENROUTER_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
