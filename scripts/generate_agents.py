import os

AGENTS = [
    "diagnosis_agent", "treatment_agent", "appointment_agent", 
    "lab_agent", "pharmacy_agent", "billing_agent", 
    "insurance_agent", "discharge_agent", "emergency_agent", 
    "notification_agent", "audit_agent"
]

BASE_DIR = "agents"

AGENT_TEMPLATE = """import json
import logging
from typing import Dict, Any

from agents.base_agent import BaseAgent
from agents.shared.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class {class_name}(BaseAgent):
    def __init__(self):
        super().__init__(name="{agent_name}")

    async def initialize(self, input_data: Dict[str, Any]) -> None:
        pass

    async def validate_input(self, input_data: Dict[str, Any]) -> None:
        pass

    async def retrieve_context(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {{}}

    async def reason(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        # Mock reasoning
        return json.dumps({{"status": "processed by {agent_name}", "next_state": "COMPLETED"}})

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any], reasoning: str) -> Dict[str, Any]:
        return json.loads(reasoning)

    async def verify(self, execution_result: Dict[str, Any]) -> None:
        pass

    async def handoff(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        return execution_result

{instance_name} = {class_name}()
"""

for agent in AGENTS:
    agent_dir = os.path.join(BASE_DIR, agent)
    os.makedirs(agent_dir, exist_ok=True)
    os.makedirs(os.path.join(agent_dir, "prompts"), exist_ok=True)
    os.makedirs(os.path.join(agent_dir, "tests"), exist_ok=True)
    
    # Class name generation (e.g. diagnosis_agent -> DiagnosisAgent)
    class_name = "".join(word.capitalize() for word in agent.split("_"))
    
    # Write agent.py
    with open(os.path.join(agent_dir, "agent.py"), "w") as f:
        f.write(AGENT_TEMPLATE.format(class_name=class_name, agent_name=agent, instance_name=agent))
        
    # Write tools.py
    with open(os.path.join(agent_dir, "tools.py"), "w") as f:
        f.write("# Tools for " + class_name + "\n")
        
    # Write schemas.py
    with open(os.path.join(agent_dir, "schemas.py"), "w") as f:
        f.write("# Schemas for " + class_name + "\n")
        
    # Write config.py
    with open(os.path.join(agent_dir, "config.py"), "w") as f:
        f.write("# Config for " + class_name + "\n")
        
    # Write prompt
    with open(os.path.join(agent_dir, "prompts", f"{agent.replace('_agent', '')}.md"), "w") as f:
        f.write("# Prompt for " + class_name + "\n")

print("Successfully generated all specialized agents.")
