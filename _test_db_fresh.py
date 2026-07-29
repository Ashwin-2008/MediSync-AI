import sys, os, asyncio, ssl
sys.modules['google._upb._message'] = None
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
sys.path.insert(0, r"d:\Third year Projects\Agentverse")

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(r"d:\Third year Projects\Agentverse\.env"))

from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text

raw = os.getenv("DATABASE_URL", "")
url = raw.replace("postgres://", "postgresql+asyncpg://").replace("postgresql://", "postgresql+asyncpg://")
parsed = urlparse(url)
qs = {k: v for k, v in parse_qs(parsed.query).items() if k != "sslmode"}
url = urlunparse(parsed._replace(query=urlencode(qs, doseq=True)))

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

engine = create_async_engine(url, connect_args={"ssl": ssl_ctx}, pool_pre_ping=True)
Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def main():
    async with Session() as db:
        print("Testing connection...")
        r = await db.execute(text("SELECT COUNT(*) FROM patients"))
        print(f"Patients: {r.scalar()}")
        r = await db.execute(text("SELECT COUNT(*) FROM users"))
        print(f"Users: {r.scalar()}")
        r = await db.execute(text("SELECT COUNT(*) FROM doctors"))
        print(f"Doctors: {r.scalar()}")
    await engine.dispose()
    print("DB OK")

asyncio.run(main())
