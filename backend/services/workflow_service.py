import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from backend import crud, schemas

class WorkflowService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_conversation(self, session_id: str) -> Optional[schemas.workflow.ConversationDetailResponse]:
        conv = await crud.conversation.get_by_session(self.db, session_id=session_id)
        if not conv:
            return None
            
        msgs = await crud.message.get_by_conversation(self.db, conversation_id=conv.id)
        
        return schemas.workflow.ConversationDetailResponse(
            **schemas.workflow.ConversationResponse.model_validate(conv).model_dump(),
            messages=[schemas.workflow.MessageResponse.model_validate(m) for m in msgs]
        )

    async def add_message(self, conversation_id: uuid.UUID, obj_in: schemas.workflow.MessageCreate) -> schemas.workflow.MessageResponse:
        msg = await crud.message.create(self.db, obj_in=obj_in)
        return schemas.workflow.MessageResponse.model_validate(msg)

    async def get_workflow_instance(self, session_id: str) -> Optional[schemas.workflow.WorkflowInstanceDetailResponse]:
        instance = await crud.workflow_instance.get_by_session(self.db, session_id=session_id)
        if not instance:
            return None
            
        executions = await crud.agent_execution.get_by_workflow(self.db, workflow_id=instance.id)
        
        return schemas.workflow.WorkflowInstanceDetailResponse(
            **schemas.workflow.WorkflowInstanceResponse.model_validate(instance).model_dump(),
            executions=[schemas.workflow.AgentExecutionResponse.model_validate(e) for e in executions]
        )
