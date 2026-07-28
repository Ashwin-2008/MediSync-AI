import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.api import deps
from backend.models.hospital import Setting
from backend.schemas.hospital import SettingResponse, SettingCreate
from backend.models.auth import User

router = APIRouter()

@router.get("/", response_model=list[SettingResponse])
async def read_settings(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve settings."""
    result = await db.execute(select(Setting).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/", response_model=SettingResponse)
async def create_setting(
    *,
    db: AsyncSession = Depends(deps.get_db),
    setting_in: SettingCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new setting."""
    setting = Setting(**setting_in.model_dump())
    db.add(setting)
    await db.commit()
    await db.refresh(setting)
    return setting
