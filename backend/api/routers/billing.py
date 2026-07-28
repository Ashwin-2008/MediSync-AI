import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_billing import invoice as crud_invoice
from backend.schemas.billing import InvoiceResponse, InvoiceCreate, InvoiceUpdate, PaginatedInvoiceResponse
from backend.models.auth import User

router = APIRouter()

@router.get("/", response_model=PaginatedInvoiceResponse)
async def read_invoices(
    db: AsyncSession = Depends(deps.get_db),
    pagination: dict = Depends(deps.get_pagination),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve invoices."""
    invoices, total = await crud_invoice.get_multi_with_count(db, skip=pagination["skip"], limit=pagination["limit"])
    return {"items": invoices, "total": total, "page": pagination["skip"] // pagination["limit"] + 1, "size": pagination["limit"]}

@router.post("/", response_model=InvoiceResponse)
async def create_invoice(
    *,
    db: AsyncSession = Depends(deps.get_db),
    invoice_in: InvoiceCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new invoice."""
    invoice = await crud_invoice.create(db, obj_in=invoice_in)
    return invoice

@router.get("/{id}", response_model=InvoiceResponse)
async def read_invoice(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get invoice by ID."""
    invoice = await crud_invoice.get(db, id=id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.put("/{id}", response_model=InvoiceResponse)
async def update_invoice(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    invoice_in: InvoiceUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update an invoice."""
    invoice = await crud_invoice.get(db, id=id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice = await crud_invoice.update(db, db_obj=invoice, obj_in=invoice_in)
    return invoice

@router.delete("/{id}", response_model=InvoiceResponse)
async def delete_invoice(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete an invoice."""
    invoice = await crud_invoice.get(db, id=id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice = await crud_invoice.remove(db, id=id)
    return invoice
