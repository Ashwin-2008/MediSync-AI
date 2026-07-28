from agents.shared.tool_registry import Tool, tool_registry

async def fetch_intake_guidelines(symptom: str) -> str:
    """Tool to fetch hospital triage guidelines for a specific symptom."""
    # In reality, this would query the knowledge base RAG
    return f"Guidelines for {symptom}: Assess severity and duration."

intake_guidelines_tool = Tool(
    name="fetch_intake_guidelines",
    description="Fetches hospital triage guidelines.",
    func=fetch_intake_guidelines,
    schema={
        "type": "object",
        "properties": {
            "symptom": {"type": "string"}
        },
        "required": ["symptom"]
    }
)

tool_registry.register(intake_guidelines_tool)
