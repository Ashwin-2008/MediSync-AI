import asyncio
import httpx
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000/api/v1"

async def test_workflows():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Login
        logger.info("Testing Login...")
        login_data = {"username": "admin@hospital.com", "password": "password123"}
        response = await client.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code != 200:
            logger.error(f"Login failed: {response.text}")
            return
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        logger.info("Login successful")

        # 2. Patient Creation (simulate frontend call)
        logger.info("Testing Patient Creation...")
        patient_payload = {
            "first_name": "Test",
            "last_name": "Patient",
            "date_of_birth": "1990-01-01",
            "gender": "Male",
            "contact_phone": "1234567890",
            "contact_email": "test@patient.com",
            "address": "123 Main St",
            "emergency_contact_name": "Jane Doe",
            "emergency_contact_phone": "0987654321"
        }
        response = await client.post(f"{BASE_URL}/patients/", json=patient_payload, headers=headers)
        if response.status_code != 200:
            logger.error(f"Patient creation failed: {response.text}")
            return
        patient_id = response.json()["id"]
        logger.info(f"Patient created successfully: {patient_id}")

        # 3. AI Workflow
        logger.info("Testing AI Workflow...")
        workflow_payload = {
            "workflow_id": "",
            "payload": {
                "message": "I have fever, cough and chest pain.",
                "patient_id": patient_id
            }
        }
        response = await client.post(f"{BASE_URL}/workflow/start", json=workflow_payload, headers=headers)
        if response.status_code != 200:
            logger.error(f"AI Workflow failed: {response.text}")
            return
        logger.info(f"AI Workflow executed successfully: {response.json()}")

        # 4. Check Database Persistence via GET lists
        logger.info("Testing Database Persistence (Dashboard / List endpoints)...")
        patients_res = await client.get(f"{BASE_URL}/patients/", headers=headers)
        if patients_res.status_code == 200 and len(patients_res.json()["items"]) > 0:
            logger.info("Patients populated in DB.")
            
        workflow_res = await client.get(f"{BASE_URL}/workflow/", headers=headers)
        if workflow_res.status_code == 200 and len(workflow_res.json()["items"]) > 0:
            logger.info("Workflows populated in DB.")
            
        logger.info("ALL END-TO-END WORKFLOWS COMPLETED SUCCESSFULLY.")

if __name__ == "__main__":
    asyncio.run(test_workflows())
