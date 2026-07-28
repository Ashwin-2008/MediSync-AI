from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import AbstractBaseModel

class Invoice(AbstractBaseModel):
    __tablename__ = "invoices"
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("appointments.id"))
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="PENDING") # PENDING, PAID, PARTIAL
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    payments: Mapped[List["Payment"]] = relationship(back_populates="invoice")
    claims: Mapped[List["InsuranceClaim"]] = relationship(back_populates="invoice")

class Payment(AbstractBaseModel):
    __tablename__ = "payments"
    invoice_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"))
    amount: Mapped[float] = mapped_column(Float)
    payment_method: Mapped[str] = mapped_column(String(50)) # CASH, CREDIT, INSURANCE
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100))
    
    invoice: Mapped["Invoice"] = relationship(back_populates="payments")

class InsuranceClaim(AbstractBaseModel):
    __tablename__ = "insurance_claims"
    invoice_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("invoices.id"))
    policy_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("insurance_policies.id"))
    claim_amount: Mapped[float] = mapped_column(Float)
    approved_amount: Mapped[Optional[float]] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50), default="SUBMITTED") # SUBMITTED, APPROVED, DENIED
    submission_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    invoice: Mapped["Invoice"] = relationship(back_populates="claims")
