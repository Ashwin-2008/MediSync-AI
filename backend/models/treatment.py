from typing import List, Optional
import uuid
from datetime import datetime, date
from sqlalchemy import String, ForeignKey, Date, DateTime, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import AbstractBaseModel

class TreatmentPlan(AbstractBaseModel):
    __tablename__ = "treatment_plans"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    doctor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("doctors.id"))
    diagnosis_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("diagnoses.id"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE")
    
    treatments: Mapped[List["Treatment"]] = relationship(back_populates="plan")

class Treatment(AbstractBaseModel):
    __tablename__ = "treatments"
    plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("treatment_plans.id", ondelete="CASCADE"))
    treatment_type: Mapped[str] = mapped_column(String(100)) # MEDICATION, SURGERY, THERAPY
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50))
    
    plan: Mapped["TreatmentPlan"] = relationship(back_populates="treatments")

class Medicine(AbstractBaseModel):
    __tablename__ = "medicines"
    name: Mapped[str] = mapped_column(String(200), index=True)
    generic_name: Mapped[Optional[str]] = mapped_column(String(200))
    manufacturer: Mapped[Optional[str]] = mapped_column(String(200))
    unit_price: Mapped[float] = mapped_column(Float, default=0.0)
    stock_quantity: Mapped[int] = mapped_column(default=0)
    
    prescriptions: Mapped[List["Prescription"]] = relationship(back_populates="medicine")
    interactions1: Mapped[List["DrugInteraction"]] = relationship("DrugInteraction", foreign_keys="[DrugInteraction.medicine_id_1]", back_populates="medicine_1")
    interactions2: Mapped[List["DrugInteraction"]] = relationship("DrugInteraction", foreign_keys="[DrugInteraction.medicine_id_2]", back_populates="medicine_2")

class DrugInteraction(AbstractBaseModel):
    __tablename__ = "drug_interactions"
    medicine_id_1: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("medicines.id"))
    medicine_id_2: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("medicines.id"))
    severity: Mapped[str] = mapped_column(String(50)) # MILD, MODERATE, SEVERE
    description: Mapped[str] = mapped_column(Text)

    medicine_1: Mapped["Medicine"] = relationship("Medicine", foreign_keys=[medicine_id_1], back_populates="interactions1")
    medicine_2: Mapped["Medicine"] = relationship("Medicine", foreign_keys=[medicine_id_2], back_populates="interactions2")

class Prescription(AbstractBaseModel):
    __tablename__ = "prescriptions"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    doctor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("doctors.id"))
    medicine_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("medicines.id"))
    treatment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("treatments.id"))
    dosage: Mapped[str] = mapped_column(String(100))
    frequency: Mapped[str] = mapped_column(String(100))
    duration_days: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE") # ACTIVE, COMPLETED, CANCELLED
    
    medicine: Mapped["Medicine"] = relationship(back_populates="prescriptions")

class LabOrder(AbstractBaseModel):
    __tablename__ = "lab_orders"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    doctor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("doctors.id"))
    test_name: Mapped[str] = mapped_column(String(200))
    priority: Mapped[str] = mapped_column(String(50)) # ROUTINE, URGENT, STAT
    status: Mapped[str] = mapped_column(String(50), default="PENDING")
    order_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    reports: Mapped[List["LabReport"]] = relationship(back_populates="order")

class LabReport(AbstractBaseModel):
    __tablename__ = "lab_reports"
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("lab_orders.id", ondelete="CASCADE"))
    technician_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    report_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    summary: Mapped[str] = mapped_column(Text)
    
    order: Mapped["LabOrder"] = relationship(back_populates="reports")
    results: Mapped[List["LabResult"]] = relationship(back_populates="report")

class LabResult(AbstractBaseModel):
    __tablename__ = "lab_results"
    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("lab_reports.id", ondelete="CASCADE"))
    parameter_name: Mapped[str] = mapped_column(String(200))
    value: Mapped[str] = mapped_column(String(100))
    unit: Mapped[str] = mapped_column(String(50))
    reference_range: Mapped[str] = mapped_column(String(100))
    is_abnormal: Mapped[bool] = mapped_column(default=False)
    
    report: Mapped["LabReport"] = relationship(back_populates="results")

class RadiologyReport(AbstractBaseModel):
    __tablename__ = "radiology_reports"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    doctor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("doctors.id"))
    scan_type: Mapped[str] = mapped_column(String(100)) # X-RAY, MRI, CT
    report_text: Mapped[str] = mapped_column(Text)
    image_urls: Mapped[Optional[dict]] = mapped_column(JSONB)
    date_performed: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class MedicalDocument(AbstractBaseModel):
    __tablename__ = "medical_documents"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    document_type: Mapped[str] = mapped_column(String(100)) # CONSENT, PREVIOUS_RECORDS
    file_url: Mapped[str] = mapped_column(String(500))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
