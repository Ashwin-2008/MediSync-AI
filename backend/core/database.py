import ssl
from typing import AsyncGenerator
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.core.config import settings

_raw_url = settings.DATABASE_URL
if not _raw_url:
    raise ValueError("DATABASE_URL is not set in the environment / .env file.")

# Normalise scheme to postgresql+asyncpg
_url = (
    _raw_url
    .replace("postgres://", "postgresql+asyncpg://")
    .replace("postgresql://", "postgresql+asyncpg://")
)

# asyncpg rejects 'sslmode' as a query parameter (that is a libpq/psycopg2 concept).
# Strip it here — SSL is enforced via the SSLContext in connect_args instead.
_parsed = urlparse(_url)
_qs = {k: v for k, v in parse_qs(_parsed.query).items() if k != "sslmode"}
DATABASE_URL = urlunparse(_parsed._replace(query=urlencode(_qs, doseq=True)))

# asyncpg requires an ssl.SSLContext — NOT the string "require"
_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args={"ssl": _ssl_ctx},
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
