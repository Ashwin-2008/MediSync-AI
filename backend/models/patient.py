from typing import List, Optional
import uuid
from datetime import date
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship as sa_relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import AbstractBaseModel

class Patient(AbstractBaseModel):
    __tablename__ = "patients"
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[date] = mapped_column(Date)
    gender: Mapped[str] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    
    profile: Mapped[Optional["PatientProfile"]] = sa_relationship(back_populates="patient", uselist=False, cascade="all, delete-orphan")
    address: Mapped[Optional["PatientAddress"]] = sa_relationship(back_populates="patient", uselist=False, cascade="all, delete-orphan")
    emergency_contacts: Mapped[List["EmergencyContact"]] = sa_relationship(back_populates="patient", cascade="all, delete-orphan")
    insurance_policies: Mapped[List["InsurancePolicy"]] = sa_relationship(back_populates="patient", cascade="all, delete-orphan")

class PatientProfile(AbstractBaseModel):
    __tablename__ = "patient_profiles"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), unique=True)
    blood_type: Mapped[Optional[str]] = mapped_column(String(5))
    marital_status: Mapped[Optional[str]] = mapped_column(String(50))
    occupation: Mapped[Optional[str]] = mapped_column(String(100))
    
    patient: Mapped["Patient"] = sa_relationship(back_populates="profile")

class PatientAddress(AbstractBaseModel):
    __tablename__ = "patient_addresses"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), unique=True)
    street: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    zip_code: Mapped[str] = mapped_column(String(20))
    country: Mapped[str] = mapped_column(String(100))
    
    patient: Mapped["Patient"] = sa_relationship(back_populates="address")

class EmergencyContact(AbstractBaseModel):
    __tablename__ = "emergency_contacts"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(200))
    relationship: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(50))
    
    patient: Mapped["Patient"] = sa_relationship(back_populates="emergency_contacts")

class InsurancePolicy(AbstractBaseModel):
    __tablename__ = "insurance_policies"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"))
    provider_name: Mapped[str] = mapped_column(String(200))
    policy_number: Mapped[str] = mapped_column(String(100), index=True)
    group_number: Mapped[Optional[str]] = mapped_column(String(100))
    valid_from: Mapped[date] = mapped_column(Date)
    valid_to: Mapped[Optional[date]] = mapped_column(Date)
    
    patient: Mapped["Patient"] = sa_relationship(back_populates="insurance_policies")
