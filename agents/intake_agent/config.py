from agents.shared.llm_factory import ModelType

INTAKE_AGENT_CONFIG = {
    "name": "intake_agent",
    "description": "Handles initial patient registration, symptom gathering, and basic triage.",
    "model": ModelType.GEMINI_FLASH,
    "max_retries": 3,
    "timeout_seconds": 30
}
