from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from agents.orchestrator.orchestrator import hospital_orchestrator
from backend.api.websockets import router as websocket_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Multi-Agent Hospital Coordination API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket_router)

class WorkflowRequest(BaseModel):
    workflow_id: str = ""
    payload: dict

@app.post("/api/v1/workflow/start")
async def start_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """Starts or continues a workflow through the orchestrator."""
    # Run the orchestrator. For long running, we can use background tasks, but here we wait for the immediate next state.
    result = await hospital_orchestrator.handle_request(request.workflow_id, request.payload)
    return result

class HumanReviewRequest(BaseModel):
    workflow_id: str
    approved: bool
    payload: dict

@app.post("/api/v1/workflow/resume")
async def resume_workflow(request: HumanReviewRequest):
    """Resumes a workflow after human review."""
    hospital_orchestrator.resume_workflow(request.workflow_id, request.approved, request.payload)
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
def health_check():
    return {"status": "healthy"}
