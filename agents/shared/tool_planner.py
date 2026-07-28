import asyncio
import logging
from typing import List, Dict, Any
from agents.shared.tool_registry import tool_registry

try:
    from tenacity import retry, stop_after_attempt, wait_exponential
except ImportError:
    # Stub tenacity if missing
    def retry(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    stop_after_attempt = lambda x: None
    wait_exponential = lambda **kwargs: None

logger = logging.getLogger(__name__)

class ToolPlanner:
    """Plans and executes tool calls efficiently with retries."""

    @staticmethod
    async def estimate_costs(tools_requested: List[str]) -> Dict[str, Any]:
        """Estimates latency and cost for requested tools."""
        return {
            "estimated_latency_ms": len(tools_requested) * 200,
            "estimated_cost_usd": len(tools_requested) * 0.001,
            "parallelizable": True
        }

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _execute_single_tool(call: Dict[str, Any]) -> Dict[str, Any]:
        name = call.get("name")
        kwargs = call.get("kwargs", {})
        try:
            tool = tool_registry.get_tool(name)
            logger.info(f"Executing tool: {name}")
            result = await tool.execute(**kwargs)
            # Ensure pydantic models are dumped to dict for json serialization
            if hasattr(result, "dict"):
                result = result.dict()
            elif hasattr(result, "model_dump"):
                result = result.model_dump()
            return {"tool": name, "status": "success", "result": result}
        except Exception as e:
            logger.error(f"Error executing tool {name}: {str(e)}")
            raise # Raise to trigger tenacity retry
            
    @staticmethod
    async def execute_parallel(tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Executes a list of tool calls concurrently, with retries on individual failures.
        """
        async def safe_execute(call):
            try:
                return await ToolPlanner._execute_single_tool(call)
            except Exception as e:
                # After all retries fail, return the error gracefully so other tools succeed
                return {"tool": call.get("name"), "status": "error", "error": str(e)}

        tasks = [safe_execute(call) for call in tool_calls]
        results = await asyncio.gather(*tasks)
        return list(results)
