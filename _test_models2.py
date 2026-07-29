import sys, os, asyncio
sys.modules['google._upb._message'] = None
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")
from openai import AsyncOpenAI

MODELS = [
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
    "openai/gpt-oss-20b:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-nano-9b-v2:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "inclusionai/ling-3.0-flash:free",
    "qwen/qwen3-8b:free",
    "qwen/qwen3-14b:free",
    "qwen/qwen3-235b-a22b:free",
]

async def test(model, key):
    client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=key, timeout=25)
    try:
        r = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": 'Patient has fever. Return JSON only: {"diagnosis":"Viral fever","confidence":0.9}'}],
            max_tokens=80,
        )
        content = r.choices[0].message.content or ""
        print(f"OK   {model}")
        print(f"     {content[:120]}")
        return model
    except Exception as e:
        print(f"FAIL {model} -> {str(e)[:100]}")
        return None

async def main():
    key = os.getenv("OPENROUTER_KEY", "").strip()
    print(f"Key: ***{key[-8:]}\n")
    for m in MODELS:
        result = await test(m, key)
        if result:
            print(f"\nWorking model: {result}")
            return
    print("\nNone worked.")

asyncio.run(main())
