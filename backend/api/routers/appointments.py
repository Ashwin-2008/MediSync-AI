import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_clinical import appointment as crud_appointment
from backend.schemas.clinical import AppointmentResponse, AppointmentCreate, AppointmentUpdate, PaginatedAppointmentResponse
from backend.models.auth import User

router = APIRouter()

@router.get("/", response_model=PaginatedAppointmentResponse)
async def read_appointments(
    db: AsyncSession = Depends(deps.get_db),
    pagination: dict = Depends(deps.get_pagination),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve appointments."""
    appointments, total = await crud_appointment.get_multi_with_count(db, skip=pagination["skip"], limit=pagination["limit"])
    return {"items": appointments, "total": total, "page": pagination["skip"] // pagination["limit"] + 1, "size": pagination["limit"]}

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    *,
    db: AsyncSession = Depends(deps.get_db),
    appointment_in: AppointmentCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new appointment."""
    appointment = await crud_appointment.create(db, obj_in=appointment_in)
    return appointment

@router.get("/{id}", response_model=AppointmentResponse)
async def read_appointment(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get appointment by ID."""
    appointment = await crud_appointment.get(db, id=id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.put("/{id}", response_model=AppointmentResponse)
async def update_appointment(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    appointment_in: AppointmentUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update an appointment."""
    appointment = await crud_appointment.get(db, id=id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment = await crud_appointment.update(db, db_obj=appointment, obj_in=appointment_in)
    return appointment

@router.delete("/{id}", response_model=AppointmentResponse)
async def delete_appointment(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete an appointment."""
    appointment = await crud_appointment.get(db, id=id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment = await crud_appointment.remove(db, id=id)
    return appointment
