import uuid
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import Field
from .base import BaseSchema, UUIDSchema, PaginationSchema

# Payment
class PaymentBase(BaseSchema):
    amount: float
    payment_method: str
    payment_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    transaction_id: Optional[str] = None

class PaymentCreate(PaymentBase):
    invoice_id: uuid.UUID

class PaymentResponse(PaymentBase, UUIDSchema):
    invoice_id: uuid.UUID

# Insurance Claim
class InsuranceClaimBase(BaseSchema):
    claim_amount: float
    approved_amount: Optional[float] = None
    status: str = "SUBMITTED"
    submission_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class InsuranceClaimCreate(InsuranceClaimBase):
    invoice_id: uuid.UUID
    policy_id: uuid.UUID

class InsuranceClaimUpdate(BaseSchema):
    approved_amount: Optional[float] = None
    status: Optional[str] = None

class InsuranceClaimResponse(InsuranceClaimBase, UUIDSchema):
    invoice_id: uuid.UUID
    policy_id: uuid.UUID

# Invoice
class InvoiceBase(BaseSchema):
    total_amount: float = 0.0
    status: str = "PENDING"
    due_date: datetime

class InvoiceCreate(InvoiceBase):
    patient_id: uuid.UUID
    appointment_id: Optional[uuid.UUID] = None

class InvoiceUpdate(BaseSchema):
    status: Optional[str] = None
    total_amount: Optional[float] = None

class InvoiceResponse(InvoiceBase, UUIDSchema):
    patient_id: uuid.UUID
    appointment_id: Optional[uuid.UUID] = None

class InvoiceDetailResponse(InvoiceResponse):
    payments: List[PaymentResponse] = []
    claims: List[InsuranceClaimResponse] = []

class PaginatedInvoiceResponse(PaginationSchema):
    items: List[InvoiceResponse]
