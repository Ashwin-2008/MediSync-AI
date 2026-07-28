import logging
from typing import Dict, Any
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class WorkflowExecutor:
    """Executes the planned action by invoking the correct agent."""
    
    def __init__(self):
        self.registered_agents: Dict[str, BaseAgent] = {}

    def register_agent(self, name: str, agent: BaseAgent):
        self.registered_agents[name] = agent

    async def execute_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if action == "human":
            logger.info("Workflow paused. Waiting for Human-In-The-Loop approval.")
            return {"status": "paused", "reason": "human_review"}
            
        if action == "none":
            logger.info("No further actions required.")
            return {"status": "completed"}
            
        agent = self.registered_agents.get(action)
        if not agent:
            raise ValueError(f"No agent registered for action: {action}")
            
        logger.info(f"Routing to agent: {action}")
        return await agent.run(payload)
