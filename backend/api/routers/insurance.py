import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_patient import insurance_policy as crud_insurance
from backend.schemas.patient import InsurancePolicyResponse, InsurancePolicyCreate, InsurancePolicyUpdate
from backend.models.auth import User

router = APIRouter()

@router.post("/", response_model=InsurancePolicyResponse)
async def create_insurance_policy(
    *,
    db: AsyncSession = Depends(deps.get_db),
    policy_in: InsurancePolicyCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new insurance policy."""
    policy = await crud_insurance.create(db, obj_in=policy_in)
    return policy

@router.get("/{id}", response_model=InsurancePolicyResponse)
async def read_insurance_policy(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get insurance policy by ID."""
    policy = await crud_insurance.get(db, id=id)
    if not policy:
        raise HTTPException(status_code=404, detail="Insurance policy not found")
    return policy

@router.put("/{id}", response_model=InsurancePolicyResponse)
async def update_insurance_policy(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    policy_in: InsurancePolicyUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update an insurance policy."""
    policy = await crud_insurance.get(db, id=id)
    if not policy:
        raise HTTPException(status_code=404, detail="Insurance policy not found")
    policy = await crud_insurance.update(db, db_obj=policy, obj_in=policy_in)
    return policy

@router.delete("/{id}", response_model=InsurancePolicyResponse)
async def delete_insurance_policy(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete an insurance policy."""
    policy = await crud_insurance.get(db, id=id)
    if not policy:
        raise HTTPException(status_code=404, detail="Insurance policy not found")
    policy = await crud_insurance.remove(db, id=id)
    return policy
