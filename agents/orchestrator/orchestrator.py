import logging
import uuid
import json
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession

from agents.shared.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class OrchestratorAIPlanner:
    def __init__(self):
        self.registered_agents = {}

    def register_agent(self, name: str, agent: Any):
        self.registered_agents[name] = agent
        logger.info(f"Orchestrator registered agent: {name}")

    async def plan_next_step(self, workflow_id: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
        """Uses LLM to decide the next best step for the workflow."""
        prompt = f"Evaluate workflow state and determine next routing. State: {json.dumps(state_data)}\n\nYou must return a JSON object with the following schema:\n{{\"next_agent\": \"agent_name\" (must be one of: 'intake_agent', 'diagnosis_agent', 'treatment_agent', 'emergency_agent', 'appointment_agent', 'billing_agent', 'none'), \"priority\": \"NORMAL\", \"workflow_state\": \"CURRENT_STATE\"}}"
        response = await LLMFactory.generate_response("orchestrator", prompt, json_mode=True)
        
        # Parse LLM response into routing instructions
        try:
            plan = json.loads(response)
            if not plan.get("next_agent"):
                raise ValueError("Missing next_agent")
        except Exception:
            # Fallback heuristic
            current_state = state_data.get("current_state", "UNKNOWN")
            next_agent = "intake_agent" if current_state == "REGISTERED" else "none"
            plan = {
                "next_agent": next_agent,
                "priority": "NORMAL",
                "workflow_state": current_state
            }
        return plan

    async def handle_request(self, db: AsyncSession, workflow_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receives workflow requests, determines required agents,
        executes them asynchronously, and aggregates outputs.
        """
        from backend.crud import workflow_instance
        from backend.schemas.workflow import WorkflowInstanceCreate, WorkflowInstanceUpdate
        
        is_new_workflow = False
        if not workflow_id:
            workflow_id = str(uuid.uuid4())
            is_new_workflow = True
            logger.info(f"Created new workflow: {workflow_id}")
            
            # Persist to DB
            try:
                wi_create = WorkflowInstanceCreate(
                    session_id=workflow_id,
                    status="STARTED",
                    context_data=payload
                )
                await workflow_instance.create(db, obj_in=wi_create)
            except Exception as e:
                logger.error(f"Failed to create WorkflowInstance: {e}")
            
        state_data = payload.copy()
        
        # Plan next routing
        plan = await self.plan_next_step(workflow_id, state_data)
        next_agent_name = plan.get("next_agent")
        
        if next_agent_name == "human":
            logger.warning(f"Workflow {workflow_id} paused for Human Review.")
            return {"status": "paused", "workflow_id": workflow_id}
            
        if next_agent_name == "none":
             try:
                 db_wi = await workflow_instance.get_by_session(db, session_id=workflow_id)
                 if db_wi:
                     await workflow_instance.update(db, db_obj=db_wi, obj_in=WorkflowInstanceUpdate(status="COMPLETED"))
             except Exception:
                 pass
             return {"status": "completed", "workflow_id": workflow_id}
             
        agent = self.registered_agents.get(next_agent_name)
        if not agent:
             raise Exception(f"Orchestrator planned for unregistered agent: {next_agent_name}")
             
        logger.info(f"Orchestrator routing to: {next_agent_name} [Priority: {plan.get('priority')}]")
        
        payload["workflow_id"] = workflow_id
        result = await agent.run(db, payload)
        result["workflow_id"] = workflow_id
        return result

hospital_orchestrator = OrchestratorAIPlanner()

# Register all refactored agents
from agents.intake_agent.agent import intake_agent
from agents.diagnosis_agent.agent import diagnosis_agent
from agents.treatment_agent.agent import treatment_agent
from agents.emergency_agent.agent import emergency_agent
from agents.pharmacy_agent.agent import pharmacy_agent
from agents.lab_agent.agent import lab_agent
from agents.appointment_agent.agent import appointment_agent
from agents.billing_agent.agent import billing_agent
from agents.insurance_agent.agent import insurance_agent

hospital_orchestrator.register_agent(intake_agent.name, intake_agent)
hospital_orchestrator.register_agent(diagnosis_agent.name, diagnosis_agent)
hospital_orchestrator.register_agent(treatment_agent.name, treatment_agent)
hospital_orchestrator.register_agent(emergency_agent.name, emergency_agent)
hospital_orchestrator.register_agent(pharmacy_agent.name, pharmacy_agent)
hospital_orchestrator.register_agent(lab_agent.name, lab_agent)
hospital_orchestrator.register_agent(appointment_agent.name, appointment_agent)
hospital_orchestrator.register_agent(billing_agent.name, billing_agent)
hospital_orchestrator.register_agent(insurance_agent.name, insurance_agent)
