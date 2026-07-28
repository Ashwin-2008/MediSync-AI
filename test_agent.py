import asyncio
from agents.diagnosis_agent.agent import diagnosis_agent

async def main():
    try:
        print("Executing DiagnosisAgent...")
        result = await diagnosis_agent.run({"payload": {"patient_id": "123", "symptoms": ["fever"]}})
        print(f"Result: {result}")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
