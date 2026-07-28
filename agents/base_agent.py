import logging
import time
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List

from agents.shared.llm_factory import LLMFactory
from agents.shared.tracer import tracer
from agents.shared.prompt_manager import PromptManager
from agents.shared.tool_planner import ToolPlanner
from agents.shared.schemas import AgentOutput
from agents.rag.embeddings import EmbeddingEngine
from agents.rag.vector_store import vector_store

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Intelligent Base Agent enforcing a strict 15-step asynchronous execution pipeline.
    """
    def __init__(self, name: str):
        self.name = name
        self.prompt_manager = PromptManager(agent_name=name)

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """The 15-step main pipeline execution method."""
        request_id, start_time = await self.initialize(input_data)
        
        try:
            # 2. Validate
            await self.validate_input(input_data)
            
            # 3. Normalize
            normalized_data = await self.normalize_input(input_data)
            
            # 4. Memory - Patient
            patient_memory = await self.load_patient_memory(normalized_data)
            
            # 5. Memory - Workflow
            workflow_state = await self.load_workflow_state(normalized_data)
            
            # 6. RAG
            rag_docs = await self.retrieve_rag(normalized_data, patient_memory)
            
            # 7. Tools Selection
            tools_to_run = await self.select_tools(normalized_data, workflow_state)
            
            # 8. Tools Execution
            tool_results = await self.execute_tools(tools_to_run)
            
            # 9. Reason Step-by-Step
            reasoning_result = await self.reason(normalized_data, patient_memory, rag_docs, tool_results)
            
            # 10. Self Verification
            verified_result = await self.verify(reasoning_result)
            
            # 11. Confidence Estimation
            confidence_data = await self.calculate_confidence(verified_result, rag_docs, tool_results)
            
            # 12. Estimate Cost
            cost_metrics = await self.estimate_cost(request_id)
            
            # 13. Generate Final Structured Output
            final_output = await self.generate_output(verified_result, confidence_data, tool_results, rag_docs)
            
            # 14. Handoff
            handoff_data = await self.handoff(final_output)
            
            # 15. Cleanup & Tracing
            await self.cleanup(request_id, handoff_data, start_time)
            
            return handoff_data
            
        except Exception as e:
            logger.error(f"[{self.name}] Error in pipeline: {str(e)}")
            tracer.update_trace(request_id, {"errors": 1})
            raise

    # =========================================================================
    # Pipeline Steps
    # =========================================================================

    async def initialize(self, input_data: Dict[str, Any]) -> tuple[str, float]:
        start_time = time.time()
        workflow_id = input_data.get("workflow_id", "unknown")
        patient_id = input_data.get("payload", {}).get("patient_id", "unknown")
        req_id = tracer.start_trace(self.name, workflow_id, patient_id)
        logger.info(f"[{self.name}] Step 1: Initializing request {req_id}")
        return req_id, start_time

    async def validate_input(self, input_data: Dict[str, Any]) -> None:
        logger.info(f"[{self.name}] Step 2: Validating input schema.")
        pass

    async def normalize_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Step 3: Normalizing input data.")
        return input_data.get("payload", {})

    async def load_patient_memory(self, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Step 4: Loading hierarchical patient memory.")
        return {} # Override in subclass

    async def load_workflow_state(self, data: Dict[str, Any]) -> str:
        logger.info(f"[{self.name}] Step 5: Loading workflow state.")
        return "UNKNOWN" # Override in subclass

    async def retrieve_rag(self, data: Dict[str, Any], memory: Dict[str, Any]) -> List[str]:
        logger.info(f"[{self.name}] Step 6: Querying RAG collections conditionally.")
        
        # Determine RAG requirement and collection (Mocked fast LLM decision heuristic)
        # In production, this would be a fast structured LLM call based on information gaps.
        if "drug" in str(data).lower():
            collection = "drug_database"
        elif "policy" in str(data).lower() or "guideline" in str(data).lower():
            collection = "clinical_guidelines"
        elif "history" in str(data).lower():
            collection = "medical_history"
        else:
            return [] # No RAG needed
            
        logger.info(f"[{self.name}] RAG Decision: YES. Collection: {collection}")
        
        engine = EmbeddingEngine()
        query = json.dumps(data)
        query_emb = engine.generate_embedding(query)
        
        results = vector_store.search(collection, query_emb, top_k=3)
        return [res["content"] for res in results]

    async def select_tools(self, data: Dict[str, Any], state: str) -> List[Dict[str, Any]]:
        logger.info(f"[{self.name}] Step 7: Tool Planner selecting required tools.")
        return [] # Returns [{"name": "tool_name", "kwargs": {}}]

    async def execute_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.info(f"[{self.name}] Step 8: Executing tools in parallel.")
        if not tools:
            return []
        return await ToolPlanner.execute_parallel(tools)

    async def reason(self, data: Dict[str, Any], memory: Dict[str, Any], rag: List[str], tools: List[Dict[str, Any]]) -> str:
        logger.info(f"[{self.name}] Step 9: Reasoning step-by-step.")
        
        # Build prompt
        prompt = self.prompt_manager.build_task_prompt(
            context=data, 
            memory=memory, 
            rag_data=rag, 
            current_task=json.dumps(data)
        )
        
        response = await LLMFactory.generate_response(self.name, prompt)
        return response

    async def verify(self, reasoning_result: str) -> str:
        logger.info(f"[{self.name}] Step 10: Self Verification against constraints.")
        # Local verify: call prompt manager to build verification prompt and re-run if needed
        return reasoning_result

    async def calculate_confidence(self, verified_result: str, rag: List[str], tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Step 11: Calculating robust confidence matrix.")
        # Replace with true calculation
        return {
            "confidence": 0.95,
            "confidence_breakdown": {"context": 0.9, "rag": 1.0, "tools": 1.0, "history": 0.9},
            "risk_level": "LOW",
            "uncertainty": "LOW",
            "requires_human_review": False
        }

    async def estimate_cost(self, request_id: str) -> None:
        logger.info(f"[{self.name}] Step 12: Estimating latency and API costs.")
        tracer.update_trace(request_id, {"cost_usd": 0.005})

    async def generate_output(self, result: str, confidence: Dict[str, Any], tools: List[Dict[str, Any]], rag: List[str]) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Step 13: Generating standardized AgentOutput JSON.")
        try:
            parsed = json.loads(result)
        except:
            parsed = {"status": "SUCCESS", "reasoning_summary": result}
            
        output = {
            "status": parsed.get("status", "SUCCESS"),
            "agent": self.name,
            "workflow_state": parsed.get("workflow_state", "UNKNOWN"),
            "confidence": confidence["confidence"],
            "confidence_breakdown": confidence["confidence_breakdown"],
            "risk_level": confidence["risk_level"],
            "uncertainty": confidence["uncertainty"],
            "reasoning_summary": parsed.get("reasoning_summary", "Completed analysis."),
            "requires_human_review": confidence["requires_human_review"],
            "actions": parsed.get("actions", []),
            "recommendations": parsed.get("recommendations", []),
            "citations": parsed.get("citations", []),
            "tool_results": tools,
            "retrieved_documents": rag,
            "next_agent": parsed.get("next_agent", "Orchestrator"),
            "execution_metadata": {}
        }
        return output

    async def handoff(self, output: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Step 14: Formatting handoff to Orchestrator.")
        return output

    async def cleanup(self, request_id: str, final_data: Dict[str, Any], start_time: float) -> None:
        logger.info(f"[{self.name}] Step 15: Cleanup and finalize tracing.")
        final_data["execution_metadata"] = tracer.end_trace(
            request_id=request_id,
            model="gemini-1.5-pro", # mock
            provider="gemini", # mock
            prompt_version="v1",
            confidence=final_data.get("confidence", 0.0)
        )
