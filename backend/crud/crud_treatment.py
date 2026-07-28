import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import CRUDBase
from backend.models.treatment import TreatmentPlan, Treatment, Medicine, Prescription, LabOrder, LabReport, LabResult
from backend.schemas.treatment import TreatmentPlanCreate, TreatmentPlanUpdate, TreatmentCreate, TreatmentUpdate, MedicineCreate, MedicineUpdate, PrescriptionCreate, PrescriptionUpdate, LabOrderCreate, LabOrderUpdate, LabReportCreate, LabReportCreate, LabResultCreate, LabResultCreate

class CRUDTreatmentPlan(CRUDBase[TreatmentPlan, TreatmentPlanCreate, TreatmentPlanUpdate]):
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> List[TreatmentPlan]:
        result = await db.execute(select(TreatmentPlan).filter(TreatmentPlan.patient_id == patient_id))
        return list(result.scalars().all())

class CRUDTreatment(CRUDBase[Treatment, TreatmentCreate, TreatmentUpdate]):
    async def get_by_plan(self, db: AsyncSession, *, plan_id: uuid.UUID) -> List[Treatment]:
        result = await db.execute(select(Treatment).filter(Treatment.plan_id == plan_id))
        return list(result.scalars().all())

class CRUDMedicine(CRUDBase[Medicine, MedicineCreate, MedicineUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Medicine]:
        result = await db.execute(select(Medicine).filter(Medicine.name == name))
        return result.scalars().first()

class CRUDPrescription(CRUDBase[Prescription, PrescriptionCreate, PrescriptionUpdate]):
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> List[Prescription]:
        result = await db.execute(select(Prescription).filter(Prescription.patient_id == patient_id))
        return list(result.scalars().all())

class CRUDLabOrder(CRUDBase[LabOrder, LabOrderCreate, LabOrderUpdate]):
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> List[LabOrder]:
        result = await db.execute(select(LabOrder).filter(LabOrder.patient_id == patient_id))
        return list(result.scalars().all())

treatment_plan = CRUDTreatmentPlan(TreatmentPlan)
treatment = CRUDTreatment(Treatment)
medicine = CRUDMedicine(Medicine)
prescription = CRUDPrescription(Prescription)
lab_order = CRUDLabOrder(LabOrder)
