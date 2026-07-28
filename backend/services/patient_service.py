import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from backend import crud, schemas
from fastapi import HTTPException

class PatientService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_patient(self, patient_id: uuid.UUID) -> Optional[schemas.patient.PatientResponse]:
        return await crud.patient.get(self.db, id=patient_id)

    async def get_patient_details(self, patient_id: uuid.UUID) -> Optional[schemas.patient.PatientDetailResponse]:
        pat = await crud.patient.get(self.db, id=patient_id)
        if not pat:
            return None
            
        profile = await crud.patient_profile.get_by_patient(self.db, patient_id=patient_id)
        address = await crud.patient_address.get_by_patient(self.db, patient_id=patient_id)
        emergency_contacts = await crud.emergency_contact.get_by_patient(self.db, patient_id=patient_id)
        insurance_policies = await crud.insurance_policy.get_by_patient(self.db, patient_id=patient_id)

        # Convert to Pydantic explicitly using from_orm/model_validate
        return schemas.patient.PatientDetailResponse(
            **schemas.patient.PatientResponse.model_validate(pat).model_dump(),
            profile=schemas.patient.PatientProfileResponse.model_validate(profile) if profile else None,
            address=schemas.patient.PatientAddressResponse.model_validate(address) if address else None,
            emergency_contacts=[schemas.patient.EmergencyContactResponse.model_validate(ec) for ec in emergency_contacts],
            insurance_policies=[schemas.patient.InsurancePolicyResponse.model_validate(ip) for ip in insurance_policies]
        )

    async def create_patient(self, obj_in: schemas.patient.PatientCreate) -> schemas.patient.PatientDetailResponse:
        existing = await crud.patient.get_by_email(self.db, email=obj_in.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        # Extract nested structures
        profile_data = obj_in.profile
        address_data = obj_in.address
        
        # Create Patient
        db_patient = await crud.patient.create(self.db, obj_in=obj_in)
        
        # Create Profile
        if profile_data:
            await crud.patient_profile.create(
                self.db, 
                obj_in=schemas.patient.PatientProfileCreate(**profile_data.model_dump(), patient_id=db_patient.id)
            )
            
        # Create Address
        if address_data:
            await crud.patient_address.create(
                self.db,
                obj_in=schemas.patient.PatientAddressCreate(**address_data.model_dump(), patient_id=db_patient.id)
            )
            
        return await self.get_patient_details(db_patient.id)
