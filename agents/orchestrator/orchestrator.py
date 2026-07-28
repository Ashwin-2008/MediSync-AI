import logging
import uuid
import json
from typing import Dict, Any, List

from agents.shared.llm_factory import LLMFactory
from agents.shared.memory.workflow_memory import WorkflowMemory
from agents.shared.prompt_manager import PromptManager

logger = logging.getLogger(__name__)

class OrchestratorAIPlanner:
    def __init__(self):
        self.prompt_manager = PromptManager(agent_name="orchestrator")
        self.registered_agents = {}

    def register_agent(self, name: str, agent: Any):
        self.registered_agents[name] = agent
        logger.info(f"Orchestrator registered agent: {name}")

    async def plan_next_step(self, workflow_id: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
        """Uses LLM to decide the next best step for the workflow."""
        prompt = self.prompt_manager.build_task_prompt(
            context=state_data,
            memory={},
            rag_data=[],
            current_task="Evaluate current workflow state and determine next routing."
        )
        # Mock decision logic; in reality calls LLMFactory
        # response = await LLMFactory.generate_response("orchestrator", prompt)
        
        current_state = state_data.get("current_state", "UNKNOWN")
        requires_human = state_data.get("requires_human_review", False)
        
        if requires_human:
             return {"next_agent": "human", "priority": "HIGH", "workflow_state": "REQUIRES_HUMAN_REVIEW"}
             
        if current_state == "REGISTERED":
            next_agent = "intake_agent"
        elif current_state == "INTAKE_COMPLETE":
            next_agent = "diagnosis_agent"
        else:
            next_agent = "none"

        return {
            "next_agent": next_agent,
            "priority": "NORMAL",
            "workflow_state": current_state
        }

    async def handle_request(self, workflow_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not workflow_id:
            workflow_id = str(uuid.uuid4())
            logger.info(f"Created new workflow: {workflow_id}")
            
        # Get memory state
        state_data = WorkflowMemory.get_workflow_state(workflow_id)
        state_data.update(payload)
        
        # Plan next routing
        plan = await self.plan_next_step(workflow_id, state_data)
        next_agent_name = plan.get("next_agent")
        
        if next_agent_name == "human":
            logger.warning(f"Workflow {workflow_id} paused for Human Review.")
            WorkflowMemory.save_workflow_state(workflow_id, "REQUIRES_HUMAN_REVIEW", payload)
            return {"status": "paused", "workflow_id": workflow_id}
            
        if next_agent_name == "none":
             return {"status": "completed", "workflow_id": workflow_id}
             
        # Route to agent
        agent = self.registered_agents.get(next_agent_name)
        if not agent:
             raise Exception(f"Orchestrator planned for unregistered agent: {next_agent_name}")
             
        logger.info(f"Orchestrator routing to: {next_agent_name} [Priority: {plan.get('priority')}]")
        
        result = await agent.run(payload)
        
        # Save new state based on agent's output
        WorkflowMemory.save_workflow_state(workflow_id, result.get("workflow_state", "UNKNOWN"), result)
        
        return result

    def resume_workflow(self, workflow_id: str, approved: bool, payload: Dict[str, Any]):
        new_state = "DIAGNOSIS_PENDING" if approved else "ERROR"
        WorkflowMemory.save_workflow_state(workflow_id, new_state, payload)
        logger.info(f"Resumed workflow {workflow_id}. Approved: {approved}")

hospital_orchestrator = OrchestratorAIPlanner()
