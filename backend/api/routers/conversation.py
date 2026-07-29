import uuid
import math
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_workflow import conversation as crud_conversation
from backend.schemas.workflow import ConversationResponse, ConversationCreate, ConversationUpdate, PaginatedConversationResponse
from backend.models.auth import User

router = APIRouter()

@router.get("/", response_model=PaginatedConversationResponse)
async def read_conversations(
    db: AsyncSession = Depends(deps.get_db),
    pagination: dict = Depends(deps.get_pagination),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve conversations."""
    conversations, total = await crud_conversation.get_multi_with_count(db, skip=pagination["skip"], limit=pagination["limit"])
    pages = math.ceil(total / pagination["limit"]) if pagination["limit"] > 0 else 0
    return {"items": conversations, "total": total, "page": pagination["skip"] // pagination["limit"] + 1, "size": pagination["limit"], "pages": pages}

@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    *,
    db: AsyncSession = Depends(deps.get_db),
    conversation_in: ConversationCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new conversation."""
    conversation = await crud_conversation.create(db, obj_in=conversation_in)
    return conversation

@router.get("/{id}", response_model=ConversationResponse)
async def read_conversation(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get conversation by ID."""
    conversation = await crud_conversation.get(db, id=id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.put("/{id}", response_model=ConversationResponse)
async def update_conversation(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    conversation_in: ConversationUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update a conversation."""
    conversation = await crud_conversation.get(db, id=id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conversation = await crud_conversation.update(db, db_obj=conversation, obj_in=conversation_in)
    return conversation

@router.delete("/{id}", response_model=ConversationResponse)
async def delete_conversation(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete a conversation."""
    conversation = await crud_conversation.get(db, id=id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conversation = await crud_conversation.remove(db, id=id)
    return conversation
