import uuid
from typing import List, Optional
from datetime import datetime, date, time
from pydantic import Field
from .base import BaseSchema, UUIDSchema, PaginationSchema

# Doctor
class DoctorBase(BaseSchema):
    specialization: str
    license_number: str
    years_of_experience: int = 0

class DoctorCreate(DoctorBase):
    user_id: uuid.UUID
    department_id: uuid.UUID

class DoctorUpdate(BaseSchema):
    department_id: Optional[uuid.UUID] = None
    specialization: Optional[str] = None
    years_of_experience: Optional[int] = None

class DoctorResponse(DoctorBase, UUIDSchema):
    user_id: uuid.UUID
    department_id: uuid.UUID

class PaginatedDoctorResponse(PaginationSchema):
    items: List[DoctorResponse]

# Doctor Schedule
class DoctorScheduleBase(BaseSchema):
    day_of_week: int
    start_time: time
    end_time: time

class DoctorScheduleCreate(DoctorScheduleBase):
    doctor_id: uuid.UUID

class DoctorScheduleUpdate(BaseSchema):
    day_of_week: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class DoctorScheduleResponse(DoctorScheduleBase, UUIDSchema):
    doctor_id: uuid.UUID

# Appointment Note
class AppointmentNoteBase(BaseSchema):
    note_text: str

class AppointmentNoteCreate(AppointmentNoteBase):
    appointment_id: uuid.UUID
    author_id: uuid.UUID

class AppointmentNoteResponse(AppointmentNoteBase, UUIDSchema):
    appointment_id: uuid.UUID
    author_id: uuid.UUID

# Vital Sign
class VitalSignBase(BaseSchema):
    temperature: Optional[float] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    oxygen_saturation: Optional[float] = None
    recorded_at: datetime = Field(default_factory=datetime.utcnow)

class VitalSignCreate(VitalSignBase):
    patient_id: uuid.UUID
    appointment_id: Optional[uuid.UUID] = None

class VitalSignResponse(VitalSignBase, UUIDSchema):
    patient_id: uuid.UUID
    appointment_id: Optional[uuid.UUID] = None

# Appointment
class AppointmentBase(BaseSchema):
    appointment_time: datetime
    status: str = "SCHEDULED"
    reason: str

class AppointmentCreate(AppointmentBase):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID

class AppointmentUpdate(BaseSchema):
    appointment_time: Optional[datetime] = None
    status: Optional[str] = None
    reason: Optional[str] = None

class AppointmentResponse(AppointmentBase, UUIDSchema):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID

class AppointmentDetailResponse(AppointmentResponse):
    notes: List[AppointmentNoteResponse] = []
    vital_signs: List[VitalSignResponse] = []

class PaginatedAppointmentResponse(PaginationSchema):
    items: List[AppointmentResponse]

# Medical History
class MedicalHistoryBase(BaseSchema):
    condition: str
    diagnosis_date: Optional[date] = None
    status: str
    notes: Optional[str] = None

class MedicalHistoryCreate(MedicalHistoryBase):
    patient_id: uuid.UUID

class MedicalHistoryUpdate(BaseSchema):
    condition: Optional[str] = None
    diagnosis_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class MedicalHistoryResponse(MedicalHistoryBase, UUIDSchema):
    patient_id: uuid.UUID

# Allergy
class AllergyBase(BaseSchema):
    allergen: str
    severity: str
    reaction: Optional[str] = None

class AllergyCreate(AllergyBase):
    patient_id: uuid.UUID

class AllergyUpdate(BaseSchema):
    severity: Optional[str] = None
    reaction: Optional[str] = None

class AllergyResponse(AllergyBase, UUIDSchema):
    patient_id: uuid.UUID

# Vaccination
class VaccinationBase(BaseSchema):
    vaccine_name: str
    date_administered: date

class VaccinationCreate(VaccinationBase):
    patient_id: uuid.UUID
    administered_by: Optional[uuid.UUID] = None

class VaccinationResponse(VaccinationBase, UUIDSchema):
    patient_id: uuid.UUID
    administered_by: Optional[uuid.UUID] = None

# Diagnosis
class DiagnosisBase(BaseSchema):
    icd10_code: str
    description: str
    is_primary: bool = True

class DiagnosisCreate(DiagnosisBase):
    patient_id: uuid.UUID
    appointment_id: Optional[uuid.UUID] = None
    doctor_id: uuid.UUID

class DiagnosisResponse(DiagnosisBase, UUIDSchema):
    patient_id: uuid.UUID
    appointment_id: Optional[uuid.UUID] = None
    doctor_id: uuid.UUID

# Symptom
class SymptomBase(BaseSchema):
    symptom_name: str
    duration: Optional[str] = None
    severity: str

class SymptomCreate(SymptomBase):
    patient_id: uuid.UUID
    appointment_id: Optional[uuid.UUID] = None

class SymptomResponse(SymptomBase, UUIDSchema):
    patient_id: uuid.UUID
    appointment_id: Optional[uuid.UUID] = None
