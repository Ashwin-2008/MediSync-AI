import logging
from typing import Dict, Any
from agents.workflow.state_machine import StateMachine, WorkflowState
from agents.workflow.planner import WorkflowPlanner
from agents.workflow.executor import WorkflowExecutor
from agents.shared.memory.workflow_memory import WorkflowMemory

logger = logging.getLogger(__name__)

class WorkflowEngine:
    def __init__(self):
        self.state_machine = StateMachine()
        self.planner = WorkflowPlanner()
        self.executor = WorkflowExecutor()
        
    async def process_workflow(self, workflow_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """The core loop of the Orchestrator."""
        
        # Load state
        state_data = WorkflowMemory.get_workflow_state(workflow_id)
        current_state_str = state_data.get("current_state", WorkflowState.REGISTERED.value)
        current_state = WorkflowState(current_state_str)
        
        # Check if we are done or paused
        if current_state in [WorkflowState.COMPLETED, WorkflowState.REQUIRES_HUMAN_REVIEW, WorkflowState.ERROR]:
            logger.info(f"Workflow {workflow_id} is in state {current_state.value}. Halting auto-processing.")
            return {"workflow_id": workflow_id, "state": current_state.value, "status": "halted"}

        # Determine next action
        next_action = self.planner.get_next_action(current_state)
        
        # Execute action
        try:
            result = await self.executor.execute_action(next_action, payload)
            
            # Agent determines the next state based on its result
            new_state_str = result.get("next_state")
            if new_state_str:
                new_state = WorkflowState(new_state_str)
                if self.state_machine.validate_transition(current_state, new_state):
                    WorkflowMemory.save_workflow_state(workflow_id, new_state.value, result.get("metadata"))
                    logger.info(f"Workflow {workflow_id} transitioned: {current_state.value} -> {new_state.value}")
                    current_state = new_state
                else:
                    logger.error(f"Workflow {workflow_id} failed state transition to {new_state.value}")
                    WorkflowMemory.save_workflow_state(workflow_id, WorkflowState.ERROR.value)
                    
            return {"workflow_id": workflow_id, "state": current_state.value, "result": result}
            
        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed during execution: {str(e)}")
            WorkflowMemory.save_workflow_state(workflow_id, WorkflowState.ERROR.value)
            return {"workflow_id": workflow_id, "state": WorkflowState.ERROR.value, "error": str(e)}

    def resume_from_human_review(self, workflow_id: str, approved: bool, payload: Dict[str, Any]):
        """Resume a workflow that was paused for human review."""
        state_data = WorkflowMemory.get_workflow_state(workflow_id)
        if state_data.get("current_state") != WorkflowState.REQUIRES_HUMAN_REVIEW.value:
            raise ValueError("Workflow is not waiting for human review.")
            
        new_state = WorkflowState.TREATMENT if approved else WorkflowState.DIAGNOSIS_PENDING
        WorkflowMemory.save_workflow_state(workflow_id, new_state.value, payload)
        logger.info(f"Human review completed for {workflow_id}. Resuming to {new_state.value}.")
