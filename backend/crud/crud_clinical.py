import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import CRUDBase
from backend.models.clinical import Doctor, DoctorSchedule, Appointment, AppointmentNote, VitalSign, MedicalHistory, Allergy, Vaccination, Diagnosis, Symptom
from backend.schemas.clinical import DoctorCreate, DoctorUpdate, DoctorScheduleCreate, DoctorScheduleUpdate, AppointmentCreate, AppointmentUpdate, AppointmentNoteCreate, AppointmentNoteCreate, VitalSignCreate, VitalSignCreate, MedicalHistoryCreate, MedicalHistoryUpdate, AllergyCreate, AllergyUpdate, VaccinationCreate, VaccinationCreate, DiagnosisCreate, DiagnosisCreate, SymptomCreate, SymptomCreate

class CRUDDoctor(CRUDBase[Doctor, DoctorCreate, DoctorUpdate]):
    async def get_by_user(self, db: AsyncSession, *, user_id: uuid.UUID) -> Optional[Doctor]:
        result = await db.execute(select(Doctor).filter(Doctor.user_id == user_id))
        return result.scalars().first()

    async def get_by_department(self, db: AsyncSession, *, department_id: uuid.UUID) -> List[Doctor]:
        result = await db.execute(select(Doctor).filter(Doctor.department_id == department_id))
        return list(result.scalars().all())

class CRUDDoctorSchedule(CRUDBase[DoctorSchedule, DoctorScheduleCreate, DoctorScheduleUpdate]):
    async def get_by_doctor(self, db: AsyncSession, *, doctor_id: uuid.UUID) -> List[DoctorSchedule]:
        result = await db.execute(select(DoctorSchedule).filter(DoctorSchedule.doctor_id == doctor_id))
        return list(result.scalars().all())

class CRUDAppointment(CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate]):
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> List[Appointment]:
        result = await db.execute(select(Appointment).filter(Appointment.patient_id == patient_id))
        return list(result.scalars().all())

    async def get_by_doctor(self, db: AsyncSession, *, doctor_id: uuid.UUID) -> List[Appointment]:
        result = await db.execute(select(Appointment).filter(Appointment.doctor_id == doctor_id))
        return list(result.scalars().all())

class CRUDVitalSign(CRUDBase[VitalSign, VitalSignCreate, VitalSignCreate]): # No update for vitals
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> List[VitalSign]:
        result = await db.execute(select(VitalSign).filter(VitalSign.patient_id == patient_id))
        return list(result.scalars().all())

class CRUDMedicalHistory(CRUDBase[MedicalHistory, MedicalHistoryCreate, MedicalHistoryUpdate]):
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> List[MedicalHistory]:
        result = await db.execute(select(MedicalHistory).filter(MedicalHistory.patient_id == patient_id))
        return list(result.scalars().all())

class CRUDDiagnosis(CRUDBase[Diagnosis, DiagnosisCreate, DiagnosisCreate]):
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> List[Diagnosis]:
        result = await db.execute(select(Diagnosis).filter(Diagnosis.patient_id == patient_id))
        return list(result.scalars().all())

doctor = CRUDDoctor(Doctor)
doctor_schedule = CRUDDoctorSchedule(DoctorSchedule)
appointment = CRUDAppointment(Appointment)
vital_sign = CRUDVitalSign(VitalSign)
medical_history = CRUDMedicalHistory(MedicalHistory)
diagnosis = CRUDDiagnosis(Diagnosis)
# Others can be added similarly (Allergy, Vaccination, Symptom, etc)
