import asyncio
import logging
import re
import time
from enum import Enum
from typing import Optional
import google.generativeai as genai
from openai import AsyncOpenAI

from agents.shared.api_manager import api_manager, Provider

logger = logging.getLogger(__name__)

LLM_CALL_TIMEOUT = 60  # seconds per network call

class ModelType(Enum):
    GEMINI_FLASH        = "gemini-2.0-flash"
    OPENROUTER_FALLBACK = "google/gemma-4-26b-a4b-it:free"  # confirmed working free model on OpenRouter

# Keys must match agent self.name exactly
AGENT_MODEL_MAP = {
    "diagnosis_agent":   ModelType.GEMINI_FLASH,
    "treatment_agent":   ModelType.GEMINI_FLASH,
    "emergency_agent":   ModelType.GEMINI_FLASH,
    "orchestrator":      ModelType.GEMINI_FLASH,
    "intake_agent":      ModelType.GEMINI_FLASH,
    "pharmacy_agent":    ModelType.GEMINI_FLASH,
    "lab_agent":         ModelType.GEMINI_FLASH,
    "appointment_agent": ModelType.GEMINI_FLASH,
    "billing_agent":     ModelType.GEMINI_FLASH,
    "insurance_agent":   ModelType.GEMINI_FLASH,
}

def _strip_markdown_json(text: str) -> str:
    text = text.strip()
    m = re.match(r"^```(?:json)?\s*([\s\S]*?)```$", text)
    return m.group(1).strip() if m else text


class LLMFactory:

    @staticmethod
    async def generate_response(
        agent_name: str,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1024,
        json_mode: bool = True,
    ) -> str:
        if json_mode and "json" not in prompt.lower():
            prompt += "\n\nRespond with valid JSON only. No markdown, no explanation."

        # ── Try Gemini first ──────────────────────────────────────────────
        gemini_key = api_manager.get_key(Provider.GEMINI)
        if gemini_key:
            try:
                result = await LLMFactory._call_gemini(
                    agent_name, gemini_key, prompt, temperature, max_tokens
                )
                return result
            except Exception as e:
                status = getattr(e, "status_code", None) or _extract_status(e)
                logger.warning(
                    "[LLM] Gemini failed for agent=%s status=%s — falling back to OpenRouter. error=%s",
                    agent_name, status, str(e)[:120],
                )
                api_manager.report_error(gemini_key, status or 500)
                # fall through to OpenRouter

        # ── Fallback: OpenRouter ──────────────────────────────────────────
        or_key = api_manager.get_key(Provider.GROQ)
        if or_key:
            try:
                result = await LLMFactory._call_openrouter(
                    agent_name, or_key, prompt, temperature, max_tokens, json_mode
                )
                return result
            except Exception as e:
                status = getattr(e, "status_code", 500)
                api_manager.report_error(or_key, status)
                logger.error(
                    "[LLM] OpenRouter also failed for agent=%s error=%s",
                    agent_name, str(e)[:200],
                )
                raise RuntimeError(f"All LLM providers failed for agent '{agent_name}': {e}") from e

        raise RuntimeError(
            f"No available API keys for agent '{agent_name}'. "
            "Add a valid GEMINI_KEY_1 or OPENROUTER_KEY to .env and restart the server."
        )

    # ── Provider implementations ──────────────────────────────────────────

    @staticmethod
    async def _call_gemini(
        agent_name: str, api_key: str, prompt: str,
        temperature: float, max_tokens: int
    ) -> str:
        t0 = time.time()
        logger.info("[LLM] agent=%s provider=gemini key=***%s", agent_name, api_key[-4:])
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name=ModelType.GEMINI_FLASH.value)
        response = await asyncio.wait_for(
            model.generate_content_async(
                prompt,
                generation_config={"temperature": temperature, "max_output_tokens": max_tokens},
            ),
            timeout=LLM_CALL_TIMEOUT,
        )
        text = _strip_markdown_json(response.text)
        logger.info("[LLM] agent=%s provider=gemini done in %.2fs", agent_name, time.time() - t0)
        return text

    @staticmethod
    async def _call_openrouter(
        agent_name: str, api_key: str, prompt: str,
        temperature: float, max_tokens: int, json_mode: bool
    ) -> str:
        t0 = time.time()
        logger.info("[LLM] agent=%s provider=openrouter key=***%s", agent_name, api_key[-4:])
        client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            timeout=LLM_CALL_TIMEOUT,
        )
        kwargs = dict(
            model=ModelType.OPENROUTER_FALLBACK.value,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        # json_object mode not supported by all free OpenRouter models — skip it
        response = await client.chat.completions.create(**kwargs)
        text = _strip_markdown_json(response.choices[0].message.content or "{}")
        logger.info("[LLM] agent=%s provider=openrouter done in %.2fs", agent_name, time.time() - t0)
        return text


def _extract_status(exc: Exception) -> Optional[int]:
    """Pull HTTP status from google-generativeai exceptions."""
    msg = str(exc)
    if "429" in msg:
        return 429
    if "403" in msg:
        return 403
    if "401" in msg:
        return 401
    return 500
