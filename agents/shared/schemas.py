from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ConfidenceBreakdown(BaseModel):
    context: float = Field(default=1.0, ge=0.0, le=1.0)
    rag: float = Field(default=1.0, ge=0.0, le=1.0)
    tools: float = Field(default=1.0, ge=0.0, le=1.0)
    history: float = Field(default=1.0, ge=0.0, le=1.0)

class AgentOutput(BaseModel):
    status: str = Field(description="SUCCESS or ERROR")
    agent: str = Field(description="Name of the agent that produced this output")
    workflow_state: str = Field(description="The updated workflow state")
    
    confidence: float = Field(ge=0.0, le=1.0, description="Overall confidence score")
    confidence_breakdown: ConfidenceBreakdown
    risk_level: str = Field(description="LOW, MEDIUM, HIGH, CRITICAL")
    uncertainty: str = Field(description="LOW, MEDIUM, HIGH")
    
    reasoning_summary: str = Field(description="Step-by-step reasoning summary")
    requires_human_review: bool = Field(default=False)
    
    actions: List[Dict[str, Any]] = Field(default_factory=list, description="List of actions taken or to be taken")
    recommendations: List[str] = Field(default_factory=list, description="Clinical or workflow recommendations")
    citations: List[str] = Field(default_factory=list, description="References to guidelines or SOPs")
    
    tool_results: List[Dict[str, Any]] = Field(default_factory=list, description="Results from executed tools")
    retrieved_documents: List[Dict[str, Any]] = Field(default_factory=list, description="RAG retrieved knowledge")
    
    next_agent: str = Field(description="Recommended next agent to handle the workflow")
    execution_metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata like tokens, latency, cost")
