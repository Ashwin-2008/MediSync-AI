import json
import uuid
import logging
from typing import Dict, Any

from agents.base_agent import BaseAgent
from agents.shared.llm_factory import LLMFactory
from agents.shared.memory.patient_memory import PatientMemory
from agents.intake_agent.schemas import PatientIntakeInput, PatientIntakeOutput
from agents.intake_agent.config import INTAKE_AGENT_CONFIG

logger = logging.getLogger(__name__)

class IntakeAgent(BaseAgent):
    def __init__(self):
        super().__init__(name=INTAKE_AGENT_CONFIG["name"])

    async def initialize(self, input_data: Dict[str, Any]) -> None:
        logger.info(f"[{self.name}] Initializing intake process.")

    async def validate_input(self, input_data: Dict[str, Any]) -> None:
        # Pydantic validation
        self.parsed_input = PatientIntakeInput(**input_data)
        logger.info(f"[{self.name}] Input validated for patient: {self.parsed_input.first_name} {self.parsed_input.last_name}")

    async def retrieve_context(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Check if patient already exists in memory
        patient_id = self.parsed_input.patient_id or str(uuid.uuid4())
        self.parsed_input.patient_id = patient_id
        
        history = PatientMemory.get_patient_state(patient_id)
        return {"history": history}

    async def reason(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        with open("agents/intake_agent/prompts/intake.md", "r") as f:
            prompt_template = f.read()
            
        prompt = prompt_template.format(
            patient_data=self.parsed_input.model_dump_json(),
            history=json.dumps(context.get("history", {}))
        )
        
        # Use LLM Factory to reason/generate triage
        response = await LLMFactory.generate_response(self.name, prompt)
        
        # Mocking JSON response since LLMFactory currently returns a mock string
        # In a real scenario, LLMFactory returns the JSON string from Gemini
        mock_response = {
            "patient_id": self.parsed_input.patient_id,
            "triage_level": "3",
            "recommended_department": "General Medicine",
            "summary": f"Patient presents with {', '.join(self.parsed_input.symptoms)} for {self.parsed_input.duration_days} days.",
            "next_state": "INTAKE_COMPLETE"
        }
        return json.dumps(mock_response)

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any], reasoning: str) -> Dict[str, Any]:
        # Parse LLM output
        try:
            result_dict = json.loads(reasoning)
            return result_dict
        except Exception as e:
            logger.error(f"[{self.name}] Failed to parse LLM reasoning: {e}")
            raise

    async def verify(self, execution_result: Dict[str, Any]) -> None:
        # Validate output schema
        output = PatientIntakeOutput(**execution_result)
        logger.info(f"[{self.name}] Output verified. Triage level: {output.triage_level}")

    async def handoff(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        # Save to memory
        PatientMemory.update_patient_state(execution_result["patient_id"], execution_result)
        return execution_result

# Instantiate for the orchestrator to import
intake_agent = IntakeAgent()
