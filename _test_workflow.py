import asyncio
import sys
sys.modules['google._upb._message'] = None
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from agents.orchestrator.orchestrator import hospital_orchestrator
from backend.core.database import engine
from sqlalchemy.ext.asyncio import AsyncSession

async def test():
    async with AsyncSession(engine) as db:
        try:
            result = await hospital_orchestrator.handle_request(
                db,
                "",
                {"type": "intake", "patient_name": "John Doe", "symptoms": "fever and headache"}
            )
            print("SUCCESS:", result)
        except Exception as e:
            print(f"ERROR ({type(e).__name__}): {e}")

asyncio.run(test())
