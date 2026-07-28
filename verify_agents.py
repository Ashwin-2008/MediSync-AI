import asyncio
import json
import os
import uuid
from backend.core.database import AsyncSessionLocal
from agents.orchestrator.orchestrator import hospital_orchestrator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_test_1(db):
    print("=========================")
    print("TEST 1: INTAKE -> DIAGNOSIS -> TREATMENT")
    print("=========================")
    
    # 1. Incoming API Request
    payload = {
        "current_state": "REGISTERED",
        "patient_id": str(uuid.uuid4()),
        "description": "I have had fever, cough and chest pain for three days."
    }
    print(f"1. Incoming Request: {json.dumps(payload, indent=2)}")
    
    # 2. Intake Phase
    print("\n--- Executing Intake Agent ---")
    intake_result = await hospital_orchestrator.handle_request(db, None, payload)
    print(f"Intake Result: {json.dumps(intake_result, indent=2)}")
    
    workflow_id = intake_result["workflow_id"]
    
    # 3. Diagnosis Phase
    print("\n--- Executing Diagnosis Agent ---")
    intake_result["current_state"] = "INTAKE_COMPLETE"
    diag_result = await hospital_orchestrator.handle_request(db, workflow_id, intake_result)
    print(f"Diagnosis Result: {json.dumps(diag_result, indent=2)}")
    
    # 4. Treatment Phase
    print("\n--- Executing Treatment Agent ---")
    diag_result["current_state"] = "DIAGNOSIS_COMPLETE"
    treatment_result = await hospital_orchestrator.handle_request(db, workflow_id, diag_result)
    print(f"Treatment Result: {json.dumps(treatment_result, indent=2)}")
    
    return workflow_id

async def run_test_2(db):
    print("\n=========================")
    print("TEST 2: APPOINTMENT")
    print("=========================")
    payload = {"current_state": "REQUEST_APPOINTMENT", "patient_id": str(uuid.uuid4()), "description": "Schedule checkup"}
    result = await hospital_orchestrator.handle_request(db, None, payload)
    print(f"Appointment Result: {json.dumps(result, indent=2)}")
    return result["workflow_id"]

async def run_test_3(db):
    print("\n=========================")
    print("TEST 3: EMERGENCY")
    print("=========================")
    payload = {"current_state": "EMERGENCY_ARRIVAL", "patient_id": str(uuid.uuid4()), "description": "Car crash trauma"}
    result = await hospital_orchestrator.handle_request(db, None, payload)
    print(f"Emergency Result: {json.dumps(result, indent=2)}")
    return result["workflow_id"]

async def run_test_4(db):
    print("\n=========================")
    print("TEST 4: BILLING")
    print("=========================")
    payload = {"current_state": "DISCHARGE", "patient_id": str(uuid.uuid4()), "description": "Generate final bill"}
    result = await hospital_orchestrator.handle_request(db, None, payload)
    print(f"Billing Result: {json.dumps(result, indent=2)}")
    return result["workflow_id"]

async def verify_db(db, workflow_id):
    from backend.crud import workflow_instance, agent_execution
    import uuid
    
    wi = await workflow_instance.get_by_session(db, session_id=workflow_id)
    print(f"\n--- Database Verification for {workflow_id} ---")
    print(f"WorkflowInstance Stored: {wi is not None}")
    
    if wi:
        executions = await agent_execution.get_by_workflow(db, workflow_id=wi.id)
        print(f"AgentExecutions Stored: {len(executions)}")
        for e in executions:
            print(f" - {e.agent_name} [{e.status}] | Output: {e.output_data}")

async def mock_plan_2(*args, **kwargs): return {"next_agent": "appointment_agent", "priority": "NORMAL", "workflow_state": "REQUEST"}
async def mock_plan_3(*args, **kwargs): return {"next_agent": "emergency_agent", "priority": "CRITICAL", "workflow_state": "EMERGENCY_ARRIVAL"}
async def mock_plan_4(*args, **kwargs): return {"next_agent": "billing_agent", "priority": "NORMAL", "workflow_state": "DISCHARGE"}

async def main():
    async with AsyncSessionLocal() as db:
        w1 = await run_test_1(db)
        await verify_db(db, w1)
        
        # Test 2
        hospital_orchestrator.plan_next_step = mock_plan_2
        w2 = await run_test_2(db)
        await verify_db(db, w2)
        
        hospital_orchestrator.plan_next_step = mock_plan_3
        w3 = await run_test_3(db)
        await verify_db(db, w3)
        
        hospital_orchestrator.plan_next_step = mock_plan_4
        w4 = await run_test_4(db)
        await verify_db(db, w4)

if __name__ == "__main__":
    asyncio.run(main())
