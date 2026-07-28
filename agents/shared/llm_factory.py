import logging
from enum import Enum
from typing import Dict, Any, Optional
from agents.shared.api_manager import api_manager, Provider

logger = logging.getLogger(__name__)

class ModelType(Enum):
    GEMINI_PRO = "gemini-1.5-pro-latest"
    GEMINI_FLASH = "gemini-1.5-flash-latest"
    GROQ_KIMI = "llama3-70b-8192" # Map Kimi K2 to closest available or actual kimi if they have it
    GROQ_SCOUT = "llama3-8b-8192" # Map Llama 4 scout

# Mapping agents to their default models
AGENT_MODEL_MAP = {
    "diagnosis": ModelType.GEMINI_PRO,
    "treatment": ModelType.GEMINI_PRO,
    "emergency": ModelType.GEMINI_PRO,
    
    "intake": ModelType.GEMINI_FLASH,
    "medical_history": ModelType.GEMINI_FLASH,
    "pharmacy": ModelType.GEMINI_FLASH,
    "lab": ModelType.GEMINI_FLASH,
    
    "appointment": ModelType.GROQ_KIMI,
    "billing": ModelType.GROQ_KIMI,
    "insurance": ModelType.GROQ_KIMI,
    "audit": ModelType.GROQ_KIMI,
    
    "notification": ModelType.GROQ_SCOUT
}

def get_provider_for_model(model: ModelType) -> Provider:
    if model in [ModelType.GEMINI_PRO, ModelType.GEMINI_FLASH]:
        return Provider.GEMINI
    return Provider.GROQ

class LLMFactory:
    
    @staticmethod
    async def generate_response(agent_name: str, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generates a response for a specific agent using the appropriate model and API key.
        """
        model = AGENT_MODEL_MAP.get(agent_name, ModelType.GEMINI_FLASH)
        provider = get_provider_for_model(model)
        
        api_key = api_manager.get_key(provider)
        if not api_key:
            raise Exception(f"No available API keys for {provider.value} to serve agent {agent_name}")
            
        logger.info(f"Agent {agent_name} using {model.value} via {provider.value} (Key: ***{api_key[-4:]})")
        
        try:
            # Here we would have the actual SDK call to Gemini/Groq
            # e.g. return await _call_gemini(model.value, api_key, prompt, context)
            
            # Simulated response for now
            return f"[{agent_name} Agent] Mock response generated using {model.value}"
            
        except Exception as e:
            # e.g., if 429
            # api_manager.report_error(api_key, 429)
            logger.error(f"Error calling {model.value}: {str(e)}")
            raise
