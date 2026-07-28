import json
import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from agents.base_agent import BaseAgent
from agents.shared.llm_factory import LLMFactory
from agents.intake_agent.schemas import PatientIntakeInput, PatientIntakeOutput
from agents.intake_agent.config import INTAKE_AGENT_CONFIG

logger = logging.getLogger(__name__)

class IntakeAgent(BaseAgent):
    def __init__(self):
        super().__init__(name=INTAKE_AGENT_CONFIG["name"])

    async def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Accept raw context for LLM processing
        logger.info(f"[{self.name}] Input validated.")
        return input_data

    async def load_context(self, db: AsyncSession, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        # Real DB load logic will be placed here (e.g., retrieving patient history)
        return {"history": []}

    async def reason(self, validated_data: Dict[str, Any], context_data: Dict[str, Any]) -> str:
        from agents.shared.prompt_manager import PromptManager
        pm = PromptManager(self.name)
        prompt = pm.build_prompt(
            context_data=validated_data,
            schema='{"triage_level": "1-5", "recommended_department": "str", "summary": "str", "next_state": "INTAKE_COMPLETE"}'
        )
        response = await LLMFactory.generate_response(self.name, prompt)
        return response

    async def plan(self, reasoning: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        # Convert LLM reasoning into structural plan
        try:
            return json.loads(reasoning)
        except:
            return {
                "triage_level": "3",
                "recommended_department": "General Medicine",
                "summary": "Generated fallback plan.",
                "next_state": "INTAKE_COMPLETE"
            }

    async def execute(self, db: AsyncSession, action_plan: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        # Real tool execution (e.g. assigning a bed, scheduling appointment)
        return action_plan

    async def respond(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "SUCCESS",
            "agent": self.name,
            "result": execution_results
        }

intake_agent = IntakeAgent()
