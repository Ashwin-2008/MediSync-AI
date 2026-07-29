import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.core.database import engine

TABLES = ['users','patients','doctors','appointments','lab_orders','invoices','insurance_claims','treatments','workflow_instances']

async def check():
    async with AsyncSession(engine) as s:
        for t in TABLES:
            try:
                r = await s.execute(text(f"SELECT COUNT(*) FROM {t}"))
                print(f"  {t:<25} {r.scalar():>6} rows")
            except Exception as e:
                print(f"  {t:<25} ERROR: {e}")

asyncio.run(check())
