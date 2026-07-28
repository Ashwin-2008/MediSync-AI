import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import Field
from .base import BaseSchema, UUIDSchema, PaginationSchema

# Message
class MessageBase(BaseSchema):
    role: str
    content: str
    metadata_json: Optional[Dict[str, Any]] = None

class MessageCreate(MessageBase):
    conversation_id: uuid.UUID

class MessageResponse(MessageBase, UUIDSchema):
    conversation_id: uuid.UUID

# Conversation
class ConversationBase(BaseSchema):
    session_id: str
    summary: Optional[str] = None

class ConversationCreate(ConversationBase):
    patient_id: Optional[uuid.UUID] = None

class ConversationUpdate(BaseSchema):
    summary: Optional[str] = None

class ConversationResponse(ConversationBase, UUIDSchema):
    patient_id: Optional[uuid.UUID] = None

class ConversationDetailResponse(ConversationResponse):
    messages: List[MessageResponse] = []

class PaginatedConversationResponse(PaginationSchema):
    items: List[ConversationResponse]

# Agent Execution
class AgentExecutionBase(BaseSchema):
    agent_name: str
    status: str
    execution_metrics: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None

class AgentExecutionCreate(AgentExecutionBase):
    workflow_id: uuid.UUID

class AgentExecutionResponse(AgentExecutionBase, UUIDSchema):
    workflow_id: uuid.UUID

# Workflow Instance
class WorkflowInstanceBase(BaseSchema):
    session_id: str
    status: str
    context_data: Optional[Dict[str, Any]] = None

class WorkflowInstanceCreate(WorkflowInstanceBase):
    patient_id: Optional[uuid.UUID] = None

class WorkflowInstanceUpdate(BaseSchema):
    status: Optional[str] = None
    context_data: Optional[Dict[str, Any]] = None

class WorkflowInstanceResponse(WorkflowInstanceBase, UUIDSchema):
    patient_id: Optional[uuid.UUID] = None

class WorkflowInstanceDetailResponse(WorkflowInstanceResponse):
    executions: List[AgentExecutionResponse] = []

class PaginatedWorkflowInstanceResponse(PaginationSchema):
    items: List[WorkflowInstanceResponse]

# System Analytics
class SystemAnalyticsBase(BaseSchema):
    metric_type: str
    metric_date: datetime
    aggregated_data: Dict[str, Any]

class SystemAnalyticsCreate(SystemAnalyticsBase):
    pass

class SystemAnalyticsResponse(SystemAnalyticsBase, UUIDSchema):
    pass
