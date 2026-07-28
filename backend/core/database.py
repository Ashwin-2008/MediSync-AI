import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

load_dotenv()

# We expect a postgresql+asyncpg URL or postgres:// which needs to be replaced
DATABASE_URL = os.environ.get("DATABASE_URL", "")
DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://").replace("postgresql://", "postgresql+asyncpg://")

# If Neon DB pooler is used, we need sslmode=require in the string for some drivers, 
# but asyncpg requires ssl parameters passed to connect_args, or handled via asyncpg native DSN parsing.
# SQLAlchemy's asyncpg dialect natively handles SSL through connection arguments or string properly if formatted well.

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    # connect_args={"ssl": "require"} # Uncomment if ssl issues occur with asyncpg
)

AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
