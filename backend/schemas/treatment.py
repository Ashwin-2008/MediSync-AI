import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from pydantic import Field
from .base import BaseSchema, UUIDSchema, PaginationSchema

# Treatment
class TreatmentBase(BaseSchema):
    treatment_type: str
    description: str
    status: str

class TreatmentCreate(TreatmentBase):
    plan_id: uuid.UUID

class TreatmentUpdate(BaseSchema):
    status: Optional[str] = None
    description: Optional[str] = None

class TreatmentResponse(TreatmentBase, UUIDSchema):
    plan_id: uuid.UUID

# Treatment Plan
class TreatmentPlanBase(BaseSchema):
    title: str
    description: str
    start_date: date
    end_date: Optional[date] = None
    status: str = "ACTIVE"

class TreatmentPlanCreate(TreatmentPlanBase):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID
    diagnosis_id: Optional[uuid.UUID] = None

class TreatmentPlanUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    end_date: Optional[date] = None
    status: Optional[str] = None

class TreatmentPlanResponse(TreatmentPlanBase, UUIDSchema):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID
    diagnosis_id: Optional[uuid.UUID] = None

class TreatmentPlanDetailResponse(TreatmentPlanResponse):
    treatments: List[TreatmentResponse] = []

class PaginatedTreatmentPlanResponse(PaginationSchema):
    items: List[TreatmentPlanResponse]

# Medicine
class MedicineBase(BaseSchema):
    name: str
    generic_name: Optional[str] = None
    manufacturer: Optional[str] = None
    unit_price: float = 0.0
    stock_quantity: int = 0

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(BaseSchema):
    unit_price: Optional[float] = None
    stock_quantity: Optional[int] = None

class MedicineResponse(MedicineBase, UUIDSchema):
    pass

class PaginatedMedicineResponse(PaginationSchema):
    items: List[MedicineResponse]

# Drug Interaction
class DrugInteractionBase(BaseSchema):
    severity: str
    description: str

class DrugInteractionCreate(DrugInteractionBase):
    medicine_id_1: uuid.UUID
    medicine_id_2: uuid.UUID

class DrugInteractionResponse(DrugInteractionBase, UUIDSchema):
    medicine_id_1: uuid.UUID
    medicine_id_2: uuid.UUID

# Prescription
class PrescriptionBase(BaseSchema):
    dosage: str
    frequency: str
    duration_days: int
    status: str = "ACTIVE"

class PrescriptionCreate(PrescriptionBase):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID
    medicine_id: uuid.UUID
    treatment_id: Optional[uuid.UUID] = None

class PrescriptionUpdate(BaseSchema):
    status: Optional[str] = None

class PrescriptionResponse(PrescriptionBase, UUIDSchema):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID
    medicine_id: uuid.UUID
    treatment_id: Optional[uuid.UUID] = None

class PaginatedPrescriptionResponse(PaginationSchema):
    items: List[PrescriptionResponse]

# Lab Result
class LabResultBase(BaseSchema):
    parameter_name: str
    value: str
    unit: str
    reference_range: str
    is_abnormal: bool = False

class LabResultCreate(LabResultBase):
    report_id: uuid.UUID

class LabResultResponse(LabResultBase, UUIDSchema):
    report_id: uuid.UUID

# Lab Report
class LabReportBase(BaseSchema):
    report_date: datetime = Field(default_factory=datetime.utcnow)
    summary: str

class LabReportCreate(LabReportBase):
    order_id: uuid.UUID
    technician_id: Optional[uuid.UUID] = None

class LabReportResponse(LabReportBase, UUIDSchema):
    order_id: uuid.UUID
    technician_id: Optional[uuid.UUID] = None

class LabReportDetailResponse(LabReportResponse):
    results: List[LabResultResponse] = []

# Lab Order
class LabOrderBase(BaseSchema):
    test_name: str
    priority: str
    status: str = "PENDING"
    order_date: datetime = Field(default_factory=datetime.utcnow)

class LabOrderCreate(LabOrderBase):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID

class LabOrderUpdate(BaseSchema):
    status: Optional[str] = None

class LabOrderResponse(LabOrderBase, UUIDSchema):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID

class LabOrderDetailResponse(LabOrderResponse):
    reports: List[LabReportResponse] = []

class PaginatedLabOrderResponse(PaginationSchema):
    items: List[LabOrderResponse]

# Radiology Report
class RadiologyReportBase(BaseSchema):
    scan_type: str
    report_text: str
    image_urls: Optional[Dict[str, Any]] = None
    date_performed: datetime = Field(default_factory=datetime.utcnow)

class RadiologyReportCreate(RadiologyReportBase):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID

class RadiologyReportResponse(RadiologyReportBase, UUIDSchema):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID

# Medical Document
class MedicalDocumentBase(BaseSchema):
    document_type: str
    file_url: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

class MedicalDocumentCreate(MedicalDocumentBase):
    patient_id: uuid.UUID

class MedicalDocumentResponse(MedicalDocumentBase, UUIDSchema):
    patient_id: uuid.UUID
