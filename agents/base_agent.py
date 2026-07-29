import logging
import time
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from agents.shared.tracer import tracer

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Intelligent Base Agent enforcing a strict 9-step asynchronous execution pipeline.
    """
    def __init__(self, name: str):
        self.name = name

    async def run(self, db: AsyncSession, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """The 9-step main pipeline execution method."""
        request_id, start_time = await self.initialize(input_data)
        
        try:
            # 2. Validate Input
            validated_data = await self.validate_input(input_data)
            
            # 3. Load Context
            context_data = await self.load_context(db, validated_data)
            context_data["workflow_id"] = input_data.get("workflow_id")
            context_data["_start_time"] = start_time
            
            # 4. Reason
            reasoning = await self.reason(validated_data, context_data)
            
            # 5. Plan
            action_plan = await self.plan(reasoning, context_data)
            
            # 6. Execute (Tools & Logic)
            execution_results = await self.execute(db, action_plan, context_data)
            
            # 7. Persist (Database State)
            await self.persist(db, execution_results, context_data)
            
            # 8. Respond
            final_response = await self.respond(execution_results)
            
            # 9. Cleanup
            await self.cleanup(request_id, start_time)
            
            return final_response
            
        except Exception as e:
            logger.error(f"[{self.name}] Error in pipeline: {str(e)}")
            tracer.update_trace(request_id, {"errors": 1})
            raise

    # =========================================================================
    # Pipeline Steps
    # =========================================================================

    async def initialize(self, input_data: Dict[str, Any]) -> Tuple[str, float]:
        start_time = time.time()
        workflow_id = input_data.get("workflow_id", "unknown")
        patient_id = input_data.get("patient_id", "unknown")
        req_id = tracer.start_trace(self.name, workflow_id, patient_id)
        logger.info(f"[{self.name}] Step 1: Initializing request {req_id}")
        return req_id, start_time

    @abstractmethod
    async def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input payload."""
        pass

    @abstractmethod
    async def load_context(self, db: AsyncSession, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Load necessary DB objects and RAG context."""
        pass

    @abstractmethod
    async def reason(self, validated_data: Dict[str, Any], context_data: Dict[str, Any]) -> str:
        """Call LLM to perform reasoning on the input and context."""
        pass

    @abstractmethod
    async def plan(self, reasoning: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse LLM output into an actionable plan."""
        pass

    @abstractmethod
    async def execute(self, db: AsyncSession, action_plan: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute any tools or logic derived from the plan."""
        pass

    async def persist(self, db: AsyncSession, execution_results: Dict[str, Any], context_data: Dict[str, Any]) -> None:
        """Persist state changes to the PostgreSQL database."""
        try:
            from backend.crud import agent_execution, workflow_instance
            from backend.schemas.workflow import AgentExecutionCreate

            # Rollback any failed transaction from a prior step before writing
            await db.rollback()

            workflow_id_str = context_data.get("workflow_id")
            if workflow_id_str:
                wi = await workflow_instance.get_by_session(db, session_id=workflow_id_str)
                if wi:
                    exec_create = AgentExecutionCreate(
                        workflow_id=wi.id,
                        agent_name=self.name,
                        status="COMPLETED",
                        output_data=execution_results,
                        execution_metrics={"duration": time.time() - context_data.get("_start_time", time.time())}
                    )
                    await agent_execution.create(db, obj_in=exec_create)
        except Exception as e:
            logger.error(f"[{self.name}] DB Persistence Error: {e}")

    @abstractmethod
    async def respond(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Format the final output payload."""
        pass

    async def cleanup(self, request_id: str, start_time: float) -> None:
        logger.info(f"[{self.name}] Step 9: Cleanup.")
        tracer.end_trace(request_id=request_id, model="gemini", provider="google", prompt_version="v1", confidence=1.0)
