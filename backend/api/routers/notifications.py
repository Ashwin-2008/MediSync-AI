import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.models.auth import User

router = APIRouter()

@router.get("/")
async def read_notifications(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve notifications for the current user."""
    return []

@router.post("/{id}/read")
async def mark_notification_read(
    id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Mark a notification as read."""
    return {"status": "success"}
