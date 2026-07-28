import uuid
from typing import List, Optional
from datetime import date
from pydantic import EmailStr, Field
from .base import BaseSchema, UUIDSchema, PaginationSchema

# Patient Profile
class PatientProfileBase(BaseSchema):
    blood_type: Optional[str] = None
    marital_status: Optional[str] = None
    occupation: Optional[str] = None

class PatientProfileCreate(PatientProfileBase):
    pass

class PatientProfileUpdate(PatientProfileBase):
    pass

class PatientProfileResponse(PatientProfileBase, UUIDSchema):
    patient_id: uuid.UUID

# Patient Address
class PatientAddressBase(BaseSchema):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

class PatientAddressCreate(PatientAddressBase):
    pass

class PatientAddressUpdate(BaseSchema):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None

class PatientAddressResponse(PatientAddressBase, UUIDSchema):
    patient_id: uuid.UUID

# Emergency Contact
class EmergencyContactBase(BaseSchema):
    name: str
    relationship: str
    phone: str

class EmergencyContactCreate(EmergencyContactBase):
    patient_id: uuid.UUID

class EmergencyContactUpdate(BaseSchema):
    name: Optional[str] = None
    relationship: Optional[str] = None
    phone: Optional[str] = None

class EmergencyContactResponse(EmergencyContactBase, UUIDSchema):
    patient_id: uuid.UUID

# Insurance Policy
class InsurancePolicyBase(BaseSchema):
    provider_name: str
    policy_number: str
    group_number: Optional[str] = None
    valid_from: date
    valid_to: Optional[date] = None

class InsurancePolicyCreate(InsurancePolicyBase):
    patient_id: uuid.UUID

class InsurancePolicyUpdate(BaseSchema):
    provider_name: Optional[str] = None
    policy_number: Optional[str] = None
    group_number: Optional[str] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None

class InsurancePolicyResponse(InsurancePolicyBase, UUIDSchema):
    patient_id: uuid.UUID

# Patient
class PatientBase(BaseSchema):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class PatientCreate(PatientBase):
    profile: Optional[PatientProfileCreate] = None
    address: Optional[PatientAddressCreate] = None

class PatientUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class PatientResponse(PatientBase, UUIDSchema):
    pass

class PatientDetailResponse(PatientResponse):
    profile: Optional[PatientProfileResponse] = None
    address: Optional[PatientAddressResponse] = None
    emergency_contacts: List[EmergencyContactResponse] = []
    insurance_policies: List[InsurancePolicyResponse] = []

class PaginatedPatientResponse(PaginationSchema):
    items: List[PatientResponse]
