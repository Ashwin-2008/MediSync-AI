import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import CRUDBase
from backend.models.billing import Invoice, Payment, InsuranceClaim
from backend.schemas.billing import InvoiceCreate, InvoiceUpdate, PaymentCreate, PaymentCreate, InsuranceClaimCreate, InsuranceClaimUpdate

class CRUDInvoice(CRUDBase[Invoice, InvoiceCreate, InvoiceUpdate]):
    async def get_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> List[Invoice]:
        result = await db.execute(select(Invoice).filter(Invoice.patient_id == patient_id))
        return list(result.scalars().all())

class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentCreate]):
    async def get_by_invoice(self, db: AsyncSession, *, invoice_id: uuid.UUID) -> List[Payment]:
        result = await db.execute(select(Payment).filter(Payment.invoice_id == invoice_id))
        return list(result.scalars().all())

class CRUDInsuranceClaim(CRUDBase[InsuranceClaim, InsuranceClaimCreate, InsuranceClaimUpdate]):
    async def get_by_invoice(self, db: AsyncSession, *, invoice_id: uuid.UUID) -> List[InsuranceClaim]:
        result = await db.execute(select(InsuranceClaim).filter(InsuranceClaim.invoice_id == invoice_id))
        return list(result.scalars().all())

invoice = CRUDInvoice(Invoice)
payment = CRUDPayment(Payment)
insurance_claim = CRUDInsuranceClaim(InsuranceClaim)
