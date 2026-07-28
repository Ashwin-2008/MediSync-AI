import pytest
import json
from agents.shared.prompt_manager import PromptManager

def test_prompt_manager_builds_correctly():
    manager = PromptManager("intake_agent", "v1")
    prompt = manager.build_task_prompt(
        context={"patient_id": "123"},
        memory={"history": []},
        rag_data=["SOP 1", "SOP 2"],
        current_task="Triage patient."
    )
    
    # Assertions to ensure prompt chaining includes all vital sections
    assert "System Persona" in prompt
    assert "Context Analysis" in prompt
    assert "patient_id: '123'" in prompt
    assert "SOP 1" in prompt
    assert "Output Requirements" in prompt

def test_agent_output_schema():
    from agents.shared.schemas import AgentOutput
    # Test valid schema construction
    out = AgentOutput(
        status="SUCCESS",
        agent="test",
        workflow_state="DONE",
        confidence=0.9,
        confidence_breakdown={"context": 1.0, "rag": 1.0, "tools": 1.0, "history": 1.0},
        risk_level="LOW",
        uncertainty="LOW",
        reasoning_summary="Tested.",
        requires_human_review=False,
        next_agent="Orchestrator"
    )
    assert out.confidence == 0.9
