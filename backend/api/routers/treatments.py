import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_treatment import treatment_plan as crud_treatment_plan
from backend.schemas.treatment import TreatmentPlanResponse, TreatmentPlanCreate, TreatmentPlanUpdate, PaginatedTreatmentPlanResponse
from backend.models.auth import User

router = APIRouter()

@router.get("/", response_model=PaginatedTreatmentPlanResponse)
async def read_treatment_plans(
    db: AsyncSession = Depends(deps.get_db),
    pagination: dict = Depends(deps.get_pagination),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve treatment plans."""
    plans, total = await crud_treatment_plan.get_multi_with_count(db, skip=pagination["skip"], limit=pagination["limit"])
    return {"items": plans, "total": total, "page": pagination["skip"] // pagination["limit"] + 1, "size": pagination["limit"]}

@router.post("/", response_model=TreatmentPlanResponse)
async def create_treatment_plan(
    *,
    db: AsyncSession = Depends(deps.get_db),
    plan_in: TreatmentPlanCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new treatment plan."""
    plan = await crud_treatment_plan.create(db, obj_in=plan_in)
    return plan

@router.get("/{id}", response_model=TreatmentPlanResponse)
async def read_treatment_plan(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get treatment plan by ID."""
    plan = await crud_treatment_plan.get(db, id=id)
    if not plan:
        raise HTTPException(status_code=404, detail="Treatment plan not found")
    return plan

@router.put("/{id}", response_model=TreatmentPlanResponse)
async def update_treatment_plan(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    plan_in: TreatmentPlanUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update a treatment plan."""
    plan = await crud_treatment_plan.get(db, id=id)
    if not plan:
        raise HTTPException(status_code=404, detail="Treatment plan not found")
    plan = await crud_treatment_plan.update(db, db_obj=plan, obj_in=plan_in)
    return plan

@router.delete("/{id}", response_model=TreatmentPlanResponse)
async def delete_treatment_plan(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete a treatment plan."""
    plan = await crud_treatment_plan.get(db, id=id)
    if not plan:
        raise HTTPException(status_code=404, detail="Treatment plan not found")
    plan = await crud_treatment_plan.remove(db, id=id)
    return plan
