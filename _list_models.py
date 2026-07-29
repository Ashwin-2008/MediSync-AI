import sys, os, asyncio
sys.modules['google._upb._message'] = None
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")

import httpx

async def main():
    key = os.getenv("OPENROUTER_KEY", "").strip()
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {key}"},
        )
        models = r.json().get("data", [])
        free = [m for m in models if str(m.get("pricing", {}).get("prompt", "1")) == "0"]
        print(f"Free models available ({len(free)}):")
        for m in free[:20]:
            print(f"  {m['id']}")

asyncio.run(main())
