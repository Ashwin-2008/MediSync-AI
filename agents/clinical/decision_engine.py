import logging
from typing import Dict, Any, List
from agents.shared.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class ClinicalDecisionEngine:
    """Core logic for Differential Diagnosis, Risk Stratification, and Treatment Recommendations."""
    
    @staticmethod
    async def generate_differential(symptoms: List[str], vitals: Dict[str, Any], history: List[str]) -> List[Dict[str, Any]]:
        logger.info("Generating differential diagnosis.")
        # In a real system, this would construct a massive structured prompt combining these inputs
        # and retrieving from RAG to provide a differential.
        return [
            {"condition": "Acute Bronchitis", "probability": 0.65, "reasoning": "Matches cough and mild fever."},
            {"condition": "Pneumonia", "probability": 0.30, "reasoning": "Cannot rule out without chest X-ray."}
        ]

    @staticmethod
    async def stratify_risk(vitals: Dict[str, Any], labs: List[Dict[str, Any]]) -> str:
        logger.info("Stratifying risk based on vitals and labs.")
        # E.g., basic heuristic for NEWS2 calculation fallback
        hr = float(vitals.get("heart_rate", 80))
        temp = float(vitals.get("temperature", 37.0))
        if hr > 130 or hr < 40 or temp > 39.1 or temp < 35.0:
            return "HIGH"
        if hr > 110 or temp > 38.0:
            return "MEDIUM"
        return "LOW"

    @staticmethod
    async def recommend_treatment(diagnosis: str, risk_level: str) -> List[str]:
        logger.info(f"Generating treatment recommendations for {diagnosis} (Risk: {risk_level}).")
        if risk_level == "HIGH":
            return ["Immediate ED admission", "IV Antibiotics", "Continuous monitoring"]
        return ["Outpatient follow-up in 48 hours", "Symptomatic relief", "Rest and hydration"]

decision_engine = ClinicalDecisionEngine()
