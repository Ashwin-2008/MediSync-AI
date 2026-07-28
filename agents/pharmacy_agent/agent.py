import json
import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from agents.base_agent import BaseAgent
from agents.shared.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class PharmacyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="pharmacy_agent")

    async def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return input_data

    async def load_context(self, db: AsyncSession, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    async def reason(self, validated_data: Dict[str, Any], context_data: Dict[str, Any]) -> str:
        response = await LLMFactory.generate_response(self.name, f"Process Prescription: {validated_data}")
        return response

    async def plan(self, reasoning: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            return json.loads(reasoning)
        except:
            return {"status": "Unknown", "next_state": "COMPLETED"}

    async def execute(self, db: AsyncSession, action_plan: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        return action_plan

    async def respond(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "SUCCESS", "agent": self.name, "result": execution_results}

pharmacy_agent = PharmacyAgent()
