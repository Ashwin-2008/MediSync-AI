import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from backend import crud, schemas
from fastapi import HTTPException

class DoctorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_doctor(self, doctor_id: uuid.UUID) -> Optional[schemas.clinical.DoctorResponse]:
        return await crud.doctor.get(self.db, id=doctor_id)

    async def get_doctor_by_user(self, user_id: uuid.UUID) -> Optional[schemas.clinical.DoctorResponse]:
        return await crud.doctor.get_by_user(self.db, user_id=user_id)

    async def list_doctors_by_department(self, department_id: uuid.UUID) -> List[schemas.clinical.DoctorResponse]:
        docs = await crud.doctor.get_by_department(self.db, department_id=department_id)
        return [schemas.clinical.DoctorResponse.model_validate(doc) for doc in docs]

    async def get_doctor_schedule(self, doctor_id: uuid.UUID) -> List[schemas.clinical.DoctorScheduleResponse]:
        schedules = await crud.doctor_schedule.get_by_doctor(self.db, doctor_id=doctor_id)
        return [schemas.clinical.DoctorScheduleResponse.model_validate(s) for s in schedules]
