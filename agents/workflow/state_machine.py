from enum import Enum
import logging

logger = logging.getLogger(__name__)

class WorkflowState(Enum):
    REGISTERED = "REGISTERED"
    INTAKE_PENDING = "INTAKE_PENDING"
    INTAKE_COMPLETE = "INTAKE_COMPLETE"
    DIAGNOSIS_PENDING = "DIAGNOSIS_PENDING"
    LAB_PENDING = "LAB_PENDING"
    LAB_COMPLETE = "LAB_COMPLETE"
    TREATMENT = "TREATMENT"
    BILLING = "BILLING"
    DISCHARGE = "DISCHARGE"
    REQUIRES_HUMAN_REVIEW = "REQUIRES_HUMAN_REVIEW"
    ERROR = "ERROR"
    COMPLETED = "COMPLETED"

class StateMachine:
    def __init__(self):
        self.transitions = {
            WorkflowState.REGISTERED: [WorkflowState.INTAKE_PENDING, WorkflowState.ERROR],
            WorkflowState.INTAKE_PENDING: [WorkflowState.INTAKE_COMPLETE, WorkflowState.ERROR],
            WorkflowState.INTAKE_COMPLETE: [WorkflowState.DIAGNOSIS_PENDING, WorkflowState.ERROR],
            WorkflowState.DIAGNOSIS_PENDING: [
                WorkflowState.LAB_PENDING, 
                WorkflowState.TREATMENT, 
                WorkflowState.REQUIRES_HUMAN_REVIEW,
                WorkflowState.ERROR
            ],
            WorkflowState.LAB_PENDING: [WorkflowState.LAB_COMPLETE, WorkflowState.ERROR],
            WorkflowState.LAB_COMPLETE: [WorkflowState.DIAGNOSIS_PENDING, WorkflowState.ERROR],
            WorkflowState.REQUIRES_HUMAN_REVIEW: [WorkflowState.DIAGNOSIS_PENDING, WorkflowState.TREATMENT, WorkflowState.ERROR],
            WorkflowState.TREATMENT: [WorkflowState.BILLING, WorkflowState.ERROR],
            WorkflowState.BILLING: [WorkflowState.DISCHARGE, WorkflowState.ERROR],
            WorkflowState.DISCHARGE: [WorkflowState.COMPLETED, WorkflowState.ERROR]
        }

    def validate_transition(self, current_state: WorkflowState, next_state: WorkflowState) -> bool:
        allowed = self.transitions.get(current_state, [])
        if next_state not in allowed:
            logger.error(f"Invalid state transition: {current_state.value} -> {next_state.value}")
            return False
        return True
