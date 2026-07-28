from typing import List
from agents.workflow.state_machine import WorkflowState
import logging

logger = logging.getLogger(__name__)

class WorkflowPlanner:
    """Plans the next steps in the workflow based on the current state."""
    
    @staticmethod
    def get_next_action(state: WorkflowState) -> str:
        """Determines the next agent to route to based on state."""
        plan_map = {
            WorkflowState.REGISTERED: "intake_agent",
            WorkflowState.INTAKE_PENDING: "intake_agent",
            WorkflowState.INTAKE_COMPLETE: "diagnosis_agent",
            WorkflowState.DIAGNOSIS_PENDING: "diagnosis_agent",
            WorkflowState.LAB_PENDING: "lab_agent",
            WorkflowState.LAB_COMPLETE: "diagnosis_agent", # Re-evaluate after labs
            WorkflowState.TREATMENT: "treatment_agent",
            WorkflowState.BILLING: "billing_agent",
            WorkflowState.DISCHARGE: "discharge_agent",
            WorkflowState.REQUIRES_HUMAN_REVIEW: "human",
            WorkflowState.COMPLETED: "none",
            WorkflowState.ERROR: "audit_agent"
        }
        
        target = plan_map.get(state, "none")
        logger.info(f"Planned next action for state {state.value}: {target}")
        return target
