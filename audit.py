import sys
import traceback
import importlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def audit_module(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        logger.info(f"[OK] {module_name}")
        return True
    except Exception as e:
        logger.error(f"[ERROR] {module_name}: {e}")
        traceback.print_exc()
        return False

def main():
    modules_to_audit = [
        # Models
        "backend.models.auth",
        "backend.models.hospital",
        "backend.models.patient",
        "backend.models.clinical",
        "backend.models.treatment",
        "backend.models.billing",
        "backend.models.workflow",
        "backend.models",
        
        # Schemas
        "backend.schemas.auth",
        "backend.schemas.hospital",
        "backend.schemas.patient",
        "backend.schemas.clinical",
        "backend.schemas.treatment",
        "backend.schemas.billing",
        "backend.schemas.workflow",
        "backend.schemas",

        # CRUD
        "backend.crud.crud_auth",
        "backend.crud.crud_hospital",
        "backend.crud.crud_patient",
        "backend.crud.crud_clinical",
        "backend.crud.crud_treatment",
        "backend.crud.crud_billing",
        "backend.crud.crud_workflow",
        "backend.crud",
        
        # Services
        "backend.services.patient_service",
        "backend.services.doctor_service",
        "backend.services.appointment_service",
        "backend.services.workflow_service",
        "backend.services",
        
        # Seeder
        "backend.seed_config",
        "backend.seed_utils",
        "backend.seeders",
        
        # AI Agents
        "agents.orchestrator.orchestrator",
        "agents.shared.llm_factory",
        "agents.shared.memory.workflow_memory"
    ]
    
    success = 0
    failed = 0
    
    print("\n--- STARTING MODULE AUDIT ---\n")
    for mod in modules_to_audit:
        if audit_module(mod):
            success += 1
        else:
            failed += 1
            
    print(f"\nAudit complete. Success: {success}, Failed: {failed}")

if __name__ == "__main__":
    main()
