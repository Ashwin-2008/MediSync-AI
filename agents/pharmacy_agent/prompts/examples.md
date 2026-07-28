# Few-Shot Examples

## Example 1 - Complex Case
**Input:** Patient presents with condition matching Complex profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "pharmacy_agent",
  "workflow_state": "PROCESSED",
  "confidence": 0.75,
  "confidence_breakdown": {
    "context": 0.9,
    "rag": 0.9,
    "tools": 0.9,
    "history": 0.9
  },
  "risk_level": "LOW",
  "uncertainty": "LOW",
  "reasoning_summary": "Processed Complex case successfully.",
  "requires_human_review": false,
  "actions": [],
  "recommendations": [],
  "citations": [],
  "tool_results": [],
  "retrieved_documents": [],
  "next_agent": "Orchestrator",
  "execution_metadata": {}
}
```

## Example 2 - Ambiguous Case
**Input:** Patient presents with condition matching Ambiguous profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "pharmacy_agent",
  "workflow_state": "PROCESSED",
  "confidence": 0.75,
  "confidence_breakdown": {
    "context": 0.9,
    "rag": 0.9,
    "tools": 0.9,
    "history": 0.9
  },
  "risk_level": "LOW",
  "uncertainty": "LOW",
  "reasoning_summary": "Processed Ambiguous case successfully.",
  "requires_human_review": true,
  "actions": [],
  "recommendations": [],
  "citations": [],
  "tool_results": [],
  "retrieved_documents": [],
  "next_agent": "Orchestrator",
  "execution_metadata": {}
}
```

## Example 3 - Missing Information Case
**Input:** Patient presents with condition matching Missing Information profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "pharmacy_agent",
  "workflow_state": "PROCESSED",
  "confidence": 0.75,
  "confidence_breakdown": {
    "context": 0.9,
    "rag": 0.9,
    "tools": 0.9,
    "history": 0.9
  },
  "risk_level": "LOW",
  "uncertainty": "HIGH",
  "reasoning_summary": "Processed Missing Information case successfully.",
  "requires_human_review": false,
  "actions": [],
  "recommendations": [],
  "citations": [],
  "tool_results": [],
  "retrieved_documents": [],
  "next_agent": "Orchestrator",
  "execution_metadata": {}
}
```

## Example 4 - Simple Case
**Input:** Patient presents with condition matching Simple profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "pharmacy_agent",
  "workflow_state": "PROCESSED",
  "confidence": 0.95,
  "confidence_breakdown": {
    "context": 0.9,
    "rag": 0.9,
    "tools": 0.9,
    "history": 0.9
  },
  "risk_level": "LOW",
  "uncertainty": "LOW",
  "reasoning_summary": "Processed Simple case successfully.",
  "requires_human_review": false,
  "actions": [],
  "recommendations": [],
  "citations": [],
  "tool_results": [],
  "retrieved_documents": [],
  "next_agent": "Orchestrator",
  "execution_metadata": {}
}
```

