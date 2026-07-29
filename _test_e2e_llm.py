import sys, os, asyncio
sys.modules['google._upb._message'] = None
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))

async def main():
    from agents.shared.llm_factory import LLMFactory
    from agents.shared.api_manager import api_manager, Provider

    # Show loaded keys
    api_manager.reload()
    print(f"Gemini keys : {len(api_manager.keys[Provider.GEMINI])}")
    print(f"OpenRouter  : {len(api_manager.keys[Provider.GROQ])}")
    print()

    prompt = '''Patient symptoms: fever 38.9C, headache, body aches, fatigue for 2 days.
Return JSON matching exactly: {"diagnosis": "string", "confidence": 0.0, "recommended_department": "string", "urgency": "low|medium|high"}'''

    print("Calling LLMFactory.generate_response for diagnosis_agent...")
    try:
        result = await LLMFactory.generate_response(
            agent_name="diagnosis_agent",
            prompt=prompt,
            json_mode=True,
        )
        print(f"\nSUCCESS:\n{result}")
    except Exception as e:
        print(f"\nFAILED: {e}")

asyncio.run(main())
