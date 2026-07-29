from typing import List, Optional
import uuid
from datetime import datetime, timezone, date, time
from sqlalchemy import String, ForeignKey, Float, DateTime, Date, Time, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import AbstractBaseModel

class Doctor(AbstractBaseModel):
    __tablename__ = "doctors"
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    department_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("departments.id"))
    specialization: Mapped[str] = mapped_column(String(100))
    license_number: Mapped[str] = mapped_column(String(100), unique=True)
    years_of_experience: Mapped[int] = mapped_column(default=0)
    
    schedules: Mapped[List["DoctorSchedule"]] = relationship(back_populates="doctor")
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="doctor")

class DoctorSchedule(AbstractBaseModel):
    __tablename__ = "doctor_schedules"
    doctor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("doctors.id", ondelete="CASCADE"))
    day_of_week: Mapped[int] = mapped_column() # 0 = Monday, 6 = Sunday
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    
    doctor: Mapped["Doctor"] = relationship(back_populates="schedules")

class Appointment(AbstractBaseModel):
    __tablename__ = "appointments"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    doctor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("doctors.id"))
    appointment_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(50), default="SCHEDULED") # SCHEDULED, COMPLETED, CANCELLED
    reason: Mapped[str] = mapped_column(String(500))
    
    doctor: Mapped["Doctor"] = relationship(back_populates="appointments")
    notes: Mapped[List["AppointmentNote"]] = relationship(back_populates="appointment")
    vital_signs: Mapped[List["VitalSign"]] = relationship(back_populates="appointment")

class AppointmentNote(AbstractBaseModel):
    __tablename__ = "appointment_notes"
    appointment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("appointments.id", ondelete="CASCADE"))
    note_text: Mapped[str] = mapped_column(Text)
    author_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    appointment: Mapped["Appointment"] = relationship(back_populates="notes")

class VitalSign(AbstractBaseModel):
    __tablename__ = "vital_signs"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("appointments.id"))
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    temperature: Mapped[Optional[float]] = mapped_column(Float) # Celsius
    blood_pressure_systolic: Mapped[Optional[int]] = mapped_column()
    blood_pressure_diastolic: Mapped[Optional[int]] = mapped_column()
    heart_rate: Mapped[Optional[int]] = mapped_column()
    respiratory_rate: Mapped[Optional[int]] = mapped_column()
    oxygen_saturation: Mapped[Optional[float]] = mapped_column(Float)
    
    appointment: Mapped["Appointment"] = relationship(back_populates="vital_signs")

class MedicalHistory(AbstractBaseModel):
    __tablename__ = "medical_history"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    condition: Mapped[str] = mapped_column(String(200))
    diagnosis_date: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50)) # ACTIVE, RESOLVED
    notes: Mapped[Optional[str]] = mapped_column(Text)

class Allergy(AbstractBaseModel):
    __tablename__ = "allergies"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    allergen: Mapped[str] = mapped_column(String(200))
    severity: Mapped[str] = mapped_column(String(50)) # MILD, MODERATE, SEVERE
    reaction: Mapped[Optional[str]] = mapped_column(String(255))

class Vaccination(AbstractBaseModel):
    __tablename__ = "vaccinations"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    vaccine_name: Mapped[str] = mapped_column(String(200))
    date_administered: Mapped[date] = mapped_column(Date)
    administered_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

class Diagnosis(AbstractBaseModel):
    __tablename__ = "diagnoses"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("appointments.id"))
    doctor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("doctors.id"))
    icd10_code: Mapped[str] = mapped_column(String(20), index=True)
    description: Mapped[str] = mapped_column(String(500))
    is_primary: Mapped[bool] = mapped_column(default=True)
    
class Symptom(AbstractBaseModel):
    __tablename__ = "symptoms"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("appointments.id"))
    symptom_name: Mapped[str] = mapped_column(String(200))
    duration: Mapped[Optional[str]] = mapped_column(String(100))
    severity: Mapped[str] = mapped_column(String(50)) # LOW, MEDIUM, HIGH
