import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class MedicalSafetyEngine:
    """Core logic for hardcoded and inferred medical safety validation."""
    
    @staticmethod
    def validate_drug_interaction(drugs: List[str]) -> Dict[str, Any]:
        """Checks for severe drug-drug interactions (DDI)."""
        logger.info(f"Checking DDI for: {drugs}")
        drugs = [d.lower() for d in drugs]
        
        # Hardcoded critical interactions list
        if "warfarin" in drugs and "aspirin" in drugs:
            return {"safe": False, "reason": "CRITICAL: High risk of severe bleeding.", "severity": "CRITICAL"}
        if "sildenafil" in drugs and "nitroglycerin" in drugs:
            return {"safe": False, "reason": "CRITICAL: Severe hypotension risk.", "severity": "CRITICAL"}
            
        return {"safe": True, "reason": "No critical interactions detected.", "severity": "LOW"}

    @staticmethod
    def validate_allergy(prescribed_drug: str, patient_allergies: List[str]) -> Dict[str, Any]:
        """Cross-references prescribed medications with known patient allergies."""
        logger.info(f"Checking allergy for {prescribed_drug} against {patient_allergies}")
        drug = prescribed_drug.lower()
        allergies = [a.lower() for a in patient_allergies]
        
        if drug in allergies:
            return {"safe": False, "reason": f"CRITICAL: Direct allergy match for {drug}.", "severity": "CRITICAL"}
            
        # Class level checks (e.g., Penicillins)
        if "penicillin" in allergies and drug in ["amoxicillin", "ampicillin", "piperacillin"]:
            return {"safe": False, "reason": f"CRITICAL: Cross-reactivity allergy match for Penicillin class.", "severity": "CRITICAL"}
            
        return {"safe": True, "reason": "No allergy conflicts detected.", "severity": "LOW"}

    @staticmethod
    def check_max_dosage(drug: str, dose_mg: float, frequency: int) -> Dict[str, Any]:
        """Checks if the total daily dose exceeds safe limits."""
        daily_dose = dose_mg * frequency
        # Simplified mock rules
        limits = {
            "acetaminophen": 4000.0,
            "ibuprofen": 3200.0
        }
        drug = drug.lower()
        if drug in limits and daily_dose > limits[drug]:
            return {"safe": False, "reason": f"CRITICAL: Dose {daily_dose}mg exceeds maximum daily limit of {limits[drug]}mg.", "severity": "HIGH"}
            
        return {"safe": True, "reason": "Dose within standard limits.", "severity": "LOW"}

safety_engine = MedicalSafetyEngine()
