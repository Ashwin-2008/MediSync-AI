import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.api import deps
from backend.models.auth import Role, User
from backend.schemas.auth import RoleResponse, RoleCreate

router = APIRouter()

@router.get("/roles", response_model=list[RoleResponse])
async def get_roles(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve all system roles."""
    result = await db.execute(select(Role))
    return result.scalars().all()

@router.post("/roles", response_model=RoleResponse)
async def create_role(
    *,
    db: AsyncSession = Depends(deps.get_db),
    role_in: RoleCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create a new role."""
    role = Role(**role_in.model_dump())
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role
