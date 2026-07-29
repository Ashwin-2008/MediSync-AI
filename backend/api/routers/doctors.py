import uuid
import math
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_clinical import doctor as crud_doctor
from backend.schemas.clinical import DoctorResponse, DoctorCreate, DoctorUpdate, PaginatedDoctorResponse
from backend.models.auth import User

router = APIRouter()

@router.get("/", response_model=PaginatedDoctorResponse)
async def read_doctors(
    db: AsyncSession = Depends(deps.get_db),
    pagination: dict = Depends(deps.get_pagination),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve doctors."""
    doctors, total = await crud_doctor.get_multi_with_count(db, skip=pagination["skip"], limit=pagination["limit"])
    pages = math.ceil(total / pagination["limit"]) if pagination["limit"] > 0 else 0
    return {"items": doctors, "total": total, "page": pagination["skip"] // pagination["limit"] + 1, "size": pagination["limit"], "pages": pages}

@router.post("/", response_model=DoctorResponse)
async def create_doctor(
    *,
    db: AsyncSession = Depends(deps.get_db),
    doctor_in: DoctorCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new doctor."""
    doctor = await crud_doctor.create(db, obj_in=doctor_in)
    return doctor

@router.get("/{id}", response_model=DoctorResponse)
async def read_doctor(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get doctor by ID."""
    doctor = await crud_doctor.get(db, id=id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.put("/{id}", response_model=DoctorResponse)
async def update_doctor(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    doctor_in: DoctorUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update a doctor."""
    doctor = await crud_doctor.get(db, id=id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor = await crud_doctor.update(db, db_obj=doctor, obj_in=doctor_in)
    return doctor

@router.delete("/{id}", response_model=DoctorResponse)
async def delete_doctor(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete a doctor."""
    doctor = await crud_doctor.get(db, id=id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor = await crud_doctor.remove(db, id=id)
    return doctor
