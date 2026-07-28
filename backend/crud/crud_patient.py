import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import CRUDBase
from backend.models.patient import Patient, PatientProfile, PatientAddress, EmergencyContact, InsurancePolicy
from backend.schemas.patient import PatientCreate, PatientUpdate, PatientProfileCreate, PatientProfileUpdate, PatientAddressCreate, PatientAddressUpdate, EmergencyContactCreate, EmergencyContactUpdate, InsurancePolicyCreate, InsurancePolicyUpdate

class CRUDPatient(CRUDBase[Patient, PatientCreate, PatientUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[Patient]:
        result = await db.execute(select(Patient).filter(Patient.email == email))
        return result.scalars().first()

class CRUDPatientProfile(CRUDBase[PatientProfile, PatientProfileCreate, PatientProfileUpdate]):
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> Optional[PatientProfile]:
        result = await db.execute(select(PatientProfile).filter(PatientProfile.patient_id == patient_id))
        return result.scalars().first()

class CRUDPatientAddress(CRUDBase[PatientAddress, PatientAddressCreate, PatientAddressUpdate]):
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> Optional[PatientAddress]:
        result = await db.execute(select(PatientAddress).filter(PatientAddress.patient_id == patient_id))
        return result.scalars().first()

class CRUDEmergencyContact(CRUDBase[EmergencyContact, EmergencyContactCreate, EmergencyContactUpdate]):
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> List[EmergencyContact]:
        result = await db.execute(select(EmergencyContact).filter(EmergencyContact.patient_id == patient_id))
        return list(result.scalars().all())

class CRUDInsurancePolicy(CRUDBase[InsurancePolicy, InsurancePolicyCreate, InsurancePolicyUpdate]):
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> List[InsurancePolicy]:
        result = await db.execute(select(InsurancePolicy).filter(InsurancePolicy.patient_id == patient_id))
        return list(result.scalars().all())

patient = CRUDPatient(Patient)
patient_profile = CRUDPatientProfile(PatientProfile)
patient_address = CRUDPatientAddress(PatientAddress)
emergency_contact = CRUDEmergencyContact(EmergencyContact)
insurance_policy = CRUDInsurancePolicy(InsurancePolicy)
