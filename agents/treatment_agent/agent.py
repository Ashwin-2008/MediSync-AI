import json
import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from agents.base_agent import BaseAgent
from agents.shared.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class TreatmentAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="treatment_agent")

    async def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return input_data

    async def load_context(self, db: AsyncSession, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    async def reason(self, validated_data: Dict[str, Any], context_data: Dict[str, Any]) -> str:
        from agents.shared.prompt_manager import PromptManager
        pm = PromptManager(self.name)
        prompt = pm.build_prompt(
            context_data=validated_data,
            schema='{"treatment_plan": "str", "medications": ["str"], "next_state": "COMPLETED"}'
        )
        response = await LLMFactory.generate_response(self.name, prompt)
        return response

    async def plan(self, reasoning: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            return json.loads(reasoning)
        except:
            return {"treatment_plan": "Unknown", "next_state": "COMPLETED"}

    async def execute(self, db: AsyncSession, action_plan: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        return action_plan

    async def respond(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "SUCCESS", "agent": self.name, "result": execution_results}

treatment_agent = TreatmentAgent()
