import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_workflow import workflow_instance as crud_workflow
from backend.schemas.workflow import WorkflowInstanceResponse, WorkflowInstanceCreate, WorkflowInstanceUpdate, PaginatedWorkflowInstanceResponse
from backend.models.auth import User

router = APIRouter()

@router.get("/", response_model=PaginatedWorkflowInstanceResponse)
async def read_workflow_instances(
    db: AsyncSession = Depends(deps.get_db),
    pagination: dict = Depends(deps.get_pagination),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve workflows."""
    workflows, total = await crud_workflow.get_multi_with_count(db, skip=pagination["skip"], limit=pagination["limit"])
    return {"items": workflows, "total": total, "page": pagination["skip"] // pagination["limit"] + 1, "size": pagination["limit"]}

@router.post("/", response_model=WorkflowInstanceResponse)
async def create_workflow_instance(
    *,
    db: AsyncSession = Depends(deps.get_db),
    workflow_in: WorkflowInstanceCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new workflow."""
    workflow = await crud_workflow.create(db, obj_in=workflow_in)
    return workflow

@router.get("/{id}", response_model=WorkflowInstanceResponse)
async def read_workflow_instance(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get workflow by ID."""
    workflow = await crud_workflow.get(db, id=id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.put("/{id}", response_model=WorkflowInstanceResponse)
async def update_workflow_instance(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    workflow_in: WorkflowInstanceUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update a workflow."""
    workflow = await crud_workflow.get(db, id=id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflow = await crud_workflow.update(db, db_obj=workflow, obj_in=workflow_in)
    return workflow

@router.delete("/{id}", response_model=WorkflowInstanceResponse)
async def delete_workflow_instance(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete a workflow."""
    workflow = await crud_workflow.get(db, id=id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflow = await crud_workflow.remove(db, id=id)
    return workflow
