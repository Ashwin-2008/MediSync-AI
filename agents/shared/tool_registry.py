import logging
from typing import Dict, Any, Callable, List

logger = logging.getLogger(__name__)

class Tool:
    def __init__(self, name: str, description: str, func: Callable, schema: Dict[str, Any]):
        self.name = name
        self.description = description
        self.func = func
        self.schema = schema

    async def execute(self, **kwargs) -> Any:
        return await self.func(**kwargs)

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        if tool.name in self._tools:
            logger.warning(f"Tool {tool.name} is already registered. Overwriting.")
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get_tool(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"Tool {name} not found in registry.")
        return self._tools[name]

    def get_tools_by_names(self, names: List[str]) -> List[Tool]:
        return [self.get_tool(name) for name in names]
        
    def get_all_schemas(self, names: List[str]) -> List[Dict[str, Any]]:
        return [self.get_tool(name).schema for name in names]

# Global singleton
tool_registry = ToolRegistry()

# Example mock tools for registration (these would typically be in their own modules)
async def mock_lab_tool(patient_id: str) -> dict:
    return {"status": "success", "data": "CBC Normal"}

tool_registry.register(Tool(
    name="lab_tool",
    description="Fetches lab results for a patient.",
    func=mock_lab_tool,
    schema={
        "type": "object",
        "properties": {
            "patient_id": {"type": "string"}
        },
        "required": ["patient_id"]
    }
))
