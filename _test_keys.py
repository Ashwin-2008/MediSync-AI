import sys, os
sys.modules['google._upb._message'] = None
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import asyncio
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

import google.generativeai as genai

KEYS = [
    os.getenv("GEMINI_KEY_1", ""),
    os.getenv("GEMINI_KEY_2", ""),
]

async def test_key(key: str, label: str):
    if not key or not key.strip():
        print(f"[{label}] SKIP — empty")
        return

    print(f"[{label}] key prefix = {key[:8]}...  length = {len(key)}")
    print(f"[{label}] Looks like valid Gemini key: {key.startswith('AIza')}")

    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        t0 = time.time()
        response = await asyncio.wait_for(
            model.generate_content_async(
                'Return exactly this JSON: {"diagnosis": "test ok", "confidence": 0.99}',
                generation_config={"temperature": 0, "max_output_tokens": 64},
            ),
            timeout=20,
        )
        elapsed = time.time() - t0
        print(f"[{label}] SUCCESS in {elapsed:.2f}s — response: {response.text[:200]}")
    except asyncio.TimeoutError:
        print(f"[{label}] TIMEOUT after 20s")
    except Exception as e:
        print(f"[{label}] ERROR ({type(e).__name__}): {e}")

async def main():
    print("=== Gemini Key Diagnostic ===\n")
    for i, key in enumerate(KEYS, 1):
        await test_key(key, f"GEMINI_KEY_{i}")
        print()

asyncio.run(main())
