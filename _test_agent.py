import asyncio
from agents.shared.llm_factory import LLMFactory

async def test():
    try:
        result = await LLMFactory.generate_response(
            "orchestrator",
            '{"type": "intake", "patient_name": "John Doe", "symptoms": "fever"}',
            json_mode=True
        )
        print("SUCCESS:", result)
    except Exception as e:
        print(f"ERROR ({type(e).__name__}): {e}")

asyncio.run(test())
