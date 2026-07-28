import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import CRUDBase
from backend.models.workflow import Conversation, Message, WorkflowInstance, AgentExecution
from backend.schemas.workflow import ConversationCreate, ConversationUpdate, MessageCreate, MessageCreate, WorkflowInstanceCreate, WorkflowInstanceUpdate, AgentExecutionCreate, AgentExecutionCreate

class CRUDConversation(CRUDBase[Conversation, ConversationCreate, ConversationUpdate]):
    async def get_by_session(self, db: AsyncSession, *, session_id: str) -> Optional[Conversation]:
        result = await db.execute(select(Conversation).filter(Conversation.session_id == session_id))
        return result.scalars().first()

class CRUDMessage(CRUDBase[Message, MessageCreate, MessageCreate]):
    async def get_by_conversation(self, db: AsyncSession, *, conversation_id: uuid.UUID) -> List[Message]:
        result = await db.execute(
            select(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        return list(result.scalars().all())

class CRUDWorkflowInstance(CRUDBase[WorkflowInstance, WorkflowInstanceCreate, WorkflowInstanceUpdate]):
    async def get_by_session(self, db: AsyncSession, *, session_id: str) -> Optional[WorkflowInstance]:
        result = await db.execute(select(WorkflowInstance).filter(WorkflowInstance.session_id == session_id))
        return result.scalars().first()

class CRUDAgentExecution(CRUDBase[AgentExecution, AgentExecutionCreate, AgentExecutionCreate]):
    async def get_by_workflow(self, db: AsyncSession, *, workflow_id: uuid.UUID) -> List[AgentExecution]:
        result = await db.execute(
            select(AgentExecution)
            .filter(AgentExecution.workflow_id == workflow_id)
            .order_by(AgentExecution.created_at)
        )
        return list(result.scalars().all())

conversation = CRUDConversation(Conversation)
message = CRUDMessage(Message)
workflow_instance = CRUDWorkflowInstance(WorkflowInstance)
agent_execution = CRUDAgentExecution(AgentExecution)
