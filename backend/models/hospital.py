from typing import List, Optional
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import AbstractBaseModel

class Setting(AbstractBaseModel):
    __tablename__ = "settings"
    key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    value: Mapped[dict] = mapped_column(JSONB)
    description: Mapped[Optional[str]] = mapped_column(String(255))

class Hospital(AbstractBaseModel):
    __tablename__ = "hospitals"
    name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(500))
    contact_email: Mapped[str] = mapped_column(String(255))
    contact_phone: Mapped[str] = mapped_column(String(50))
    
    departments: Mapped[List["Department"]] = relationship(back_populates="hospital")

class Department(AbstractBaseModel):
    __tablename__ = "departments"
    hospital_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("hospitals.id"))
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    
    hospital: Mapped["Hospital"] = relationship(back_populates="departments")
    rooms: Mapped[List["Room"]] = relationship(back_populates="department")

class Room(AbstractBaseModel):
    __tablename__ = "rooms"
    department_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("departments.id"))
    room_number: Mapped[str] = mapped_column(String(20), index=True)
    room_type: Mapped[str] = mapped_column(String(50)) # ICU, GENERAL, ER
    capacity: Mapped[int] = mapped_column(Integer, default=1)
    
    department: Mapped["Department"] = relationship(back_populates="rooms")
    beds: Mapped[List["Bed"]] = relationship(back_populates="room")

class Bed(AbstractBaseModel):
    __tablename__ = "beds"
    room_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rooms.id"))
    bed_number: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(50), default="AVAILABLE") # AVAILABLE, OCCUPIED, MAINTENANCE
    
    room: Mapped["Room"] = relationship(back_populates="beds")
    admissions: Mapped[List["Admission"]] = relationship(back_populates="bed")

class Admission(AbstractBaseModel):
    __tablename__ = "admissions"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    bed_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("beds.id"))
    admission_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reason: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50), default="ADMITTED") # ADMITTED, DISCHARGED
    
    bed: Mapped["Bed"] = relationship(back_populates="admissions")
    discharge: Mapped[Optional["Discharge"]] = relationship(back_populates="admission", uselist=False)

class Discharge(AbstractBaseModel):
    __tablename__ = "discharges"
    admission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("admissions.id", ondelete="CASCADE"), unique=True)
    discharge_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    summary: Mapped[str] = mapped_column(String)
    instructions: Mapped[Optional[str]] = mapped_column(String)
    
    admission: Mapped["Admission"] = relationship(back_populates="discharge")
