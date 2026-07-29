import uuid
import math
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_treatment import lab_order as crud_lab_order
from backend.schemas.treatment import LabOrderResponse, LabOrderCreate, LabOrderUpdate, PaginatedLabOrderResponse
from backend.models.auth import User

router = APIRouter()

@router.get("/", response_model=PaginatedLabOrderResponse)
async def read_lab_orders(
    db: AsyncSession = Depends(deps.get_db),
    pagination: dict = Depends(deps.get_pagination),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve lab orders."""
    orders, total = await crud_lab_order.get_multi_with_count(db, skip=pagination["skip"], limit=pagination["limit"])
    pages = math.ceil(total / pagination["limit"]) if pagination["limit"] > 0 else 0
    return {"items": orders, "total": total, "page": pagination["skip"] // pagination["limit"] + 1, "size": pagination["limit"], "pages": pages}

@router.post("/", response_model=LabOrderResponse)
async def create_lab_order(
    *,
    db: AsyncSession = Depends(deps.get_db),
    order_in: LabOrderCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new lab order."""
    order = await crud_lab_order.create(db, obj_in=order_in)
    return order

@router.get("/{id}", response_model=LabOrderResponse)
async def read_lab_order(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get lab order by ID."""
    order = await crud_lab_order.get(db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Lab order not found")
    return order

@router.put("/{id}", response_model=LabOrderResponse)
async def update_lab_order(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    order_in: LabOrderUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update a lab order."""
    order = await crud_lab_order.get(db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Lab order not found")
    order = await crud_lab_order.update(db, db_obj=order, obj_in=order_in)
    return order

@router.delete("/{id}", response_model=LabOrderResponse)
async def delete_lab_order(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete a lab order."""
    order = await crud_lab_order.get(db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Lab order not found")
    order = await crud_lab_order.remove(db, id=id)
    return order
