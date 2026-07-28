import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from backend import crud, schemas
from fastapi import HTTPException

class AppointmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_appointment_details(self, appointment_id: uuid.UUID) -> Optional[schemas.clinical.AppointmentDetailResponse]:
        appt = await crud.appointment.get(self.db, id=appointment_id)
        if not appt:
            return None
            
        # Get notes (need CRUD for notes, skipping detailed expansion for brevity)
        return schemas.clinical.AppointmentDetailResponse.model_validate(appt)

    async def schedule_appointment(self, obj_in: schemas.clinical.AppointmentCreate) -> schemas.clinical.AppointmentResponse:
        # Check doctor exists
        doc = await crud.doctor.get(self.db, id=obj_in.doctor_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Doctor not found")
            
        # Check patient exists
        pat = await crud.patient.get(self.db, id=obj_in.patient_id)
        if not pat:
            raise HTTPException(status_code=404, detail="Patient not found")
            
        appt = await crud.appointment.create(self.db, obj_in=obj_in)
        return schemas.clinical.AppointmentResponse.model_validate(appt)

    async def list_patient_appointments(self, patient_id: uuid.UUID) -> List[schemas.clinical.AppointmentResponse]:
        appts = await crud.appointment.get_by_patient(self.db, patient_id=patient_id)
        return [schemas.clinical.AppointmentResponse.model_validate(a) for a in appts]

    async def list_doctor_appointments(self, doctor_id: uuid.UUID) -> List[schemas.clinical.AppointmentResponse]:
        appts = await crud.appointment.get_by_doctor(self.db, doctor_id=doctor_id)
        return [schemas.clinical.AppointmentResponse.model_validate(a) for a in appts]
