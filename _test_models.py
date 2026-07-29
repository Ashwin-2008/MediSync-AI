import sys, os
sys.modules['google._upb._message'] = None
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import asyncio
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")

FREE_MODELS = [
    "meta-llama/llama-3.2-3b-instruct:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "google/gemma-2-9b-it:free",
    "qwen/qwen-2.5-7b-instruct:free",
    "deepseek/deepseek-r1-0528:free",
    "microsoft/phi-3-mini-128k-instruct:free",
]

async def test(model: str, key: str):
    from openai import AsyncOpenAI
    client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=key, timeout=20)
    try:
        r = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": 'Say {"ok": true}'}],
            max_tokens=20,
        )
        print(f"  OK  {model} -> {r.choices[0].message.content}")
        return model
    except Exception as e:
        print(f"  FAIL {model} -> {str(e)[:80]}")
        return None

async def main():
    key = os.getenv("OPENROUTER_KEY", "").strip()
    print(f"Testing key ***{key[-8:]} against {len(FREE_MODELS)} free models...\n")
    for m in FREE_MODELS:
        result = await test(m, key)
        if result:
            print(f"\n✓ Use this model: {result}")
            return
    print("\nNo free model worked.")

asyncio.run(main())
