import uuid
import math
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_patient import patient as crud_patient
from backend.schemas.patient import PatientResponse, PatientCreate, PatientUpdate, PaginatedPatientResponse
from backend.models.auth import User

router = APIRouter()

@router.get("/", response_model=PaginatedPatientResponse)
async def read_patients(
    db: AsyncSession = Depends(deps.get_db),
    pagination: dict = Depends(deps.get_pagination),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve patients."""
    patients, total = await crud_patient.get_multi_with_count(db, skip=pagination["skip"], limit=pagination["limit"])
    pages = math.ceil(total / pagination["limit"]) if pagination["limit"] > 0 else 0
    return {"items": patients, "total": total, "page": pagination["skip"] // pagination["limit"] + 1, "size": pagination["limit"], "pages": pages}

@router.post("/", response_model=PatientResponse)
async def create_patient(
    *,
    db: AsyncSession = Depends(deps.get_db),
    patient_in: PatientCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new patient."""
    patient = await crud_patient.create(db, obj_in=patient_in)
    return patient

@router.get("/{id}", response_model=PatientResponse)
async def read_patient(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get patient by ID."""
    patient = await crud_patient.get(db, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{id}", response_model=PatientResponse)
async def update_patient(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    patient_in: PatientUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update a patient."""
    patient = await crud_patient.get(db, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient = await crud_patient.update(db, db_obj=patient, obj_in=patient_in)
    return patient

@router.delete("/{id}", response_model=PatientResponse)
async def delete_patient(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete a patient."""
    patient = await crud_patient.get(db, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient = await crud_patient.remove(db, id=id)
    return patient
