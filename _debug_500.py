import sys, asyncio
sys.path.insert(0, 'd:/Third year Projects/Agentverse')

from backend.core.database import AsyncSessionLocal
from sqlalchemy import text

async def test():
    try:
        async with AsyncSessionLocal() as db:
            r = await db.execute(text("SELECT COUNT(*) FROM patients"))
            print("patients count:", r.scalar())
            r2 = await db.execute(text("SELECT COUNT(*) FROM treatment_plans"))
            print("treatment_plans count:", r2.scalar())
    except Exception as e:
        print("DB ERROR:", type(e).__name__, str(e))

asyncio.run(test())
