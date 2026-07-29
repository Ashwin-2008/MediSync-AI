import sys, os
sys.modules['google._upb._message'] = None
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import asyncio
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

async def test_openrouter():
    key = os.getenv("OPENROUTER_KEY", "").strip()
    if not key:
        print("ERROR: OPENROUTER_KEY is empty in .env")
        return

    print(f"OpenRouter key: ***{key[-8:]}")

    from openai import AsyncOpenAI
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key,
        timeout=30,
    )
    try:
        response = await client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct:free",
            messages=[{"role": "user", "content":
                'Patient has fever and headache. Return JSON: {"diagnosis": "...", "confidence": 0.9}'}],
            temperature=0.2,
            max_tokens=200,
        )
        print("SUCCESS:", response.choices[0].message.content)
    except Exception as e:
        print(f"ERROR ({type(e).__name__}): {e}")

asyncio.run(test_openrouter())
