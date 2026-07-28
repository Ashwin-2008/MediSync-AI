import logging
from typing import Dict, Any, List
from .fhir_models import FHIRPatient, FHIRCondition

logger = logging.getLogger(__name__)

class InteropAdapter:
    """Base Adapter for external hospital systems."""
    def connect(self) -> bool:
        raise NotImplementedError

class HISAdapter(InteropAdapter):
    """Adapter for Hospital Information System."""
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        
    def connect(self) -> bool:
        logger.info(f"Connected to HIS at {self.endpoint}")
        return True
        
    def fetch_patient(self, patient_id: str) -> FHIRPatient:
        # Mock HIS fetch converting to FHIR format
        logger.info(f"Fetching PT from HIS: {patient_id}")
        return FHIRPatient(
            id=patient_id,
            name=[{"family": "Doe", "given": ["John"]}],
            gender="male",
            birthDate="1980-01-01"
        )

class EMRAdapter(InteropAdapter):
    """Adapter for Electronic Medical Record."""
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        
    def connect(self) -> bool:
        logger.info(f"Connected to EMR at {self.endpoint}")
        return True

    def fetch_conditions(self, patient_id: str) -> List[FHIRCondition]:
        logger.info(f"Fetching conditions from EMR for PT: {patient_id}")
        return [
            FHIRCondition(
                id="cond-123",
                code={"coding": [{"system": "http://hl7.org/fhir/sid/icd-10", "code": "J45.909"}], "text": "Asthma"},
                subject={"reference": f"Patient/{patient_id}"}
            )
        ]

class LISAdapter(InteropAdapter):
    """Adapter for Laboratory Information System."""
    def fetch_labs(self, patient_id: str) -> List[Dict[str, Any]]:
        logger.info(f"Fetching lab results from LIS for PT: {patient_id}")
        return [{"test": "Hemoglobin", "value": "14.5 g/dL", "flag": "Normal"}]
