import os
import json
from typing import Dict, Any, List

class PromptManager:
    """Dynamically constructs production complex prompt chains."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.prompts_dir = f"agents/{agent_name}/prompts"

    def _read_file(self, filename: str) -> str:
        filepath = os.path.join(self.prompts_dir, filename)
        if not os.path.exists(filepath):
            # Fallback to shared prompts if agent-specific doesn't exist
            shared_filepath = os.path.join("agents/shared/prompts", filename)
            if os.path.exists(shared_filepath):
                with open(shared_filepath, 'r') as f:
                    return f.read()
            return ""
        with open(filepath, 'r') as f:
            return f.read()

    def build_prompt(
        self, 
        context_data: Dict[str, Any], 
        hospital_context: str = "",
        patient_history: str = "",
        conversation: str = "",
        workflow_state: str = "",
        schema: str = "{}"
    ) -> str:
        """Assembles the full prompt required for Phase 4."""
        system_prompt = self._read_file("system.md")
        developer_prompt = self._read_file("developer.md")
        user_prompt = self._read_file("user.md")

        assembled_prompt = f"""{system_prompt}

{developer_prompt}

## Hospital Context
{hospital_context}

## Patient History
{patient_history}

## Previous Conversation
{conversation}

## Workflow State
{workflow_state}

## Current Input Data
{json.dumps(context_data, indent=2)}

## JSON Output Schema
You must respond with valid JSON perfectly matching this schema:
{schema}

{user_prompt}
"""
        return assembled_prompt
