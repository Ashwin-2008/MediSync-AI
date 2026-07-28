# Few-Shot Examples

## Example 1 - Complex Case
**Input:** Patient presents with condition matching Complex profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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
  "agent": "diagnosis_agent",
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
  "agent": "diagnosis_agent",
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

## Example 4 - Conflicting Reports Case
**Input:** Patient presents with condition matching Conflicting Reports profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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
  "reasoning_summary": "Processed Conflicting Reports case successfully.",
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

## Example 5 - Emergency Case
**Input:** Patient presents with condition matching Emergency profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
  "workflow_state": "PROCESSED",
  "confidence": 0.75,
  "confidence_breakdown": {
    "context": 0.9,
    "rag": 0.9,
    "tools": 0.9,
    "history": 0.9
  },
  "risk_level": "HIGH",
  "uncertainty": "LOW",
  "reasoning_summary": "Processed Emergency case successfully.",
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

## Example 6 - Invalid Request Case
**Input:** Patient presents with condition matching Invalid Request profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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
  "reasoning_summary": "Processed Invalid Request case successfully.",
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

## Example 7 - Simple Case
**Input:** Patient presents with condition matching Simple profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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

## Example 8 - Complex Case
**Input:** Patient presents with condition matching Complex profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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

## Example 9 - Ambiguous Case
**Input:** Patient presents with condition matching Ambiguous profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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

## Example 10 - Missing Information Case
**Input:** Patient presents with condition matching Missing Information profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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

## Example 11 - Conflicting Reports Case
**Input:** Patient presents with condition matching Conflicting Reports profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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
  "reasoning_summary": "Processed Conflicting Reports case successfully.",
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

## Example 12 - Emergency Case
**Input:** Patient presents with condition matching Emergency profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
  "workflow_state": "PROCESSED",
  "confidence": 0.75,
  "confidence_breakdown": {
    "context": 0.9,
    "rag": 0.9,
    "tools": 0.9,
    "history": 0.9
  },
  "risk_level": "HIGH",
  "uncertainty": "LOW",
  "reasoning_summary": "Processed Emergency case successfully.",
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

## Example 13 - Invalid Request Case
**Input:** Patient presents with condition matching Invalid Request profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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
  "reasoning_summary": "Processed Invalid Request case successfully.",
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

## Example 14 - Simple Case
**Input:** Patient presents with condition matching Simple profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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

## Example 15 - Complex Case
**Input:** Patient presents with condition matching Complex profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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

## Example 16 - Ambiguous Case
**Input:** Patient presents with condition matching Ambiguous profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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

## Example 17 - Missing Information Case
**Input:** Patient presents with condition matching Missing Information profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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

## Example 18 - Conflicting Reports Case
**Input:** Patient presents with condition matching Conflicting Reports profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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
  "reasoning_summary": "Processed Conflicting Reports case successfully.",
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

## Example 19 - Emergency Case
**Input:** Patient presents with condition matching Emergency profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
  "workflow_state": "PROCESSED",
  "confidence": 0.75,
  "confidence_breakdown": {
    "context": 0.9,
    "rag": 0.9,
    "tools": 0.9,
    "history": 0.9
  },
  "risk_level": "HIGH",
  "uncertainty": "LOW",
  "reasoning_summary": "Processed Emergency case successfully.",
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

## Example 20 - Invalid Request Case
**Input:** Patient presents with condition matching Invalid Request profile.
**Output:**
```json
{
  "status": "SUCCESS",
  "agent": "diagnosis_agent",
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
  "reasoning_summary": "Processed Invalid Request case successfully.",
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

