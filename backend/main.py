import os
import sys
import asyncio
import time
# Prevent Python from attempting to load the incompatible C extension 'google._upb._message'
sys.modules['google._upb._message'] = None
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from backend.core.config import settings
from backend.core.database import AsyncSessionLocal
from backend.core.limiter import limiter
from backend.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from agents.orchestrator.orchestrator import hospital_orchestrator
from backend.api.websockets import router as websocket_router
from backend.api.routers import (
    auth_router, patients_router, doctors_router, appointments_router,
    treatments_router, labs_router, billing_router, insurance_router,
    notifications_router, workflow_router, conversation_router,
    analytics_router, settings_router, admin_router
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Multi-Agent Hospital Coordination API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket_router)

# Register API v1 Routers
api_v1_prefix = "/api/v1"
app.include_router(auth_router, prefix=f"{api_v1_prefix}/auth", tags=["Authentication"])
app.include_router(patients_router, prefix=f"{api_v1_prefix}/patients", tags=["Patients"])
app.include_router(doctors_router, prefix=f"{api_v1_prefix}/doctors", tags=["Doctors"])
app.include_router(appointments_router, prefix=f"{api_v1_prefix}/appointments", tags=["Appointments"])
app.include_router(treatments_router, prefix=f"{api_v1_prefix}/treatments", tags=["Treatments"])
app.include_router(labs_router, prefix=f"{api_v1_prefix}/labs", tags=["Labs"])
app.include_router(billing_router, prefix=f"{api_v1_prefix}/billing", tags=["Billing"])
app.include_router(insurance_router, prefix=f"{api_v1_prefix}/insurance", tags=["Insurance"])
app.include_router(notifications_router, prefix=f"{api_v1_prefix}/notifications", tags=["Notifications"])
app.include_router(workflow_router, prefix=f"{api_v1_prefix}/workflow", tags=["Workflow Instances"])
app.include_router(conversation_router, prefix=f"{api_v1_prefix}/conversation", tags=["Conversations"])
app.include_router(analytics_router, prefix=f"{api_v1_prefix}/analytics", tags=["Analytics"])
app.include_router(settings_router, prefix=f"{api_v1_prefix}/settings", tags=["Settings"])
app.include_router(admin_router, prefix=f"{api_v1_prefix}/admin", tags=["Admin"])

class WorkflowRequest(BaseModel):
    workflow_id: str = ""
    payload: dict

@app.post("/api/v1/workflow/start")
async def start_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """Starts or continues a workflow through the orchestrator."""
    t0 = time.time()
    async with AsyncSessionLocal() as db:
        try:
            result = await hospital_orchestrator.handle_request(db, request.workflow_id, request.payload)
            logger.info("[workflow/start] completed in %.2fs", time.time() - t0)
            return result
        except asyncio.TimeoutError:
            logger.error("[workflow/start] timed out after %.1fs", time.time() - t0)
            raise HTTPException(status_code=504, detail="AI service timed out. Please try again.")
        except Exception as e:
            logger.error("[workflow/start] error: %s", str(e))
            raise HTTPException(status_code=500, detail=str(e))

class HumanReviewRequest(BaseModel):
    workflow_id: str
    approved: bool
    payload: dict

@app.post("/api/v1/workflow/resume")
async def resume_workflow(request: HumanReviewRequest):
    """Resumes a workflow after human review."""
    await hospital_orchestrator.resume_workflow(request.workflow_id, request.approved, request.payload)
    return {"status": "resumed", "workflow_id": request.workflow_id}

@app.websocket("/api/v1/ws/{workflow_id}")
async def websocket_endpoint(websocket: WebSocket, workflow_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # In a real system, the orchestrator/event bus would push state updates here.
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        logger.info("Client disconnected")

@app.get("/health")
async def health_check(db: AsyncSession = Depends(deps.get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "online"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "database": "offline"}
