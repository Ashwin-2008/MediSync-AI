import logging
import json
from enum import Enum
from typing import Dict, Any, Optional
import google.generativeai as genai
from openai import AsyncOpenAI
import tenacity

from agents.shared.api_manager import api_manager, Provider

logger = logging.getLogger(__name__)

class ModelType(Enum):
    GEMINI_PRO = "gemini-pro" # fallback to 1.0 pro
    GEMINI_FLASH = "gemini-pro"
    OPENROUTER_FALLBACK = "openai/gpt-3.5-turbo"

# Mapping agents to their default models
AGENT_MODEL_MAP = {
    "diagnosis": ModelType.GEMINI_PRO,
    "treatment": ModelType.GEMINI_PRO,
    "emergency": ModelType.GEMINI_PRO,
    "orchestrator": ModelType.GEMINI_PRO,
    
    "intake": ModelType.GEMINI_FLASH,
    "pharmacy": ModelType.GEMINI_FLASH,
    "lab": ModelType.GEMINI_FLASH,
    "appointment": ModelType.GEMINI_FLASH,
    "billing": ModelType.GEMINI_FLASH,
    "insurance": ModelType.GEMINI_FLASH,
}

def get_provider_for_model(model: ModelType) -> Provider:
    if model in [ModelType.GEMINI_PRO, ModelType.GEMINI_FLASH]:
        return Provider.GEMINI
    return Provider.GROQ # using GROQ enum to represent OpenRouter as fallback in API Manager

class LLMFactory:
    
    @staticmethod
    @tenacity.retry(
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_exception_type(Exception),
        reraise=True
    )
    async def generate_response(
        agent_name: str, 
        prompt: str, 
        temperature: float = 0.2,
        max_tokens: int = 2048,
        json_mode: bool = True
    ) -> str:
        """
        Generates a response using Gemini (Primary) or OpenRouter (Fallback).
        """
        model_enum = AGENT_MODEL_MAP.get(agent_name, ModelType.GEMINI_FLASH)
        provider = get_provider_for_model(model_enum)
        
        api_key = api_manager.get_key(provider)
        if not api_key:
            # Try forcing fallback if original provider has no keys
            provider = Provider.GROQ if provider == Provider.GEMINI else Provider.GEMINI
            api_key = api_manager.get_key(provider)
            model_enum = ModelType.OPENROUTER_FALLBACK
            
            if not api_key:
                raise Exception(f"No available API keys for {agent_name}")
                
        logger.info(f"Agent {agent_name} calling {model_enum.value} (Key: ***{api_key[-4:]})")
        
        try:
            if json_mode and "json" not in prompt.lower():
                prompt += "\n\nPlease output in JSON format."
                
            if provider == Provider.GEMINI:
                genai.configure(api_key=api_key)
                
                generation_config = {
                    "temperature": temperature,
                    "max_output_tokens": max_tokens
                }
                
                model = genai.GenerativeModel(model_name=model_enum.value)
                # Note: google.generativeai async support uses generate_content_async
                response = await model.generate_content_async(
                    prompt, 
                    generation_config=generation_config
                )
                
                text = response.text
                if text.startswith("```json"):
                    text = text.strip("```json").strip("```")
                elif text.startswith("```"):
                    text = text.strip("```")
                return text
                
            else:
                # OpenRouter Fallback using OpenAI SDK
                client = AsyncOpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key,
                )
                
                response = await client.chat.completions.create(
                    model=model_enum.value,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format={"type": "json_object"} if json_mode else None
                )
                return response.choices[0].message.content or "{}"
                
        except Exception as e:
            # Report 429s or 500s to cooldown the key
            status_code = getattr(e, 'status_code', 500)
            api_manager.report_error(api_key, status_code)
            logger.error(f"Error calling {model_enum.value}: {str(e)}")
            raise
