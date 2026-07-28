import logging
from typing import Dict, Any, List
from .schemas import *

logger = logging.getLogger(__name__)

class PatientTools:
    @staticmethod
    async def search_patient(request: PatientSearchRequest) -> PatientSearchResult:
        # Mock database lookup
        logger.info(f"Searching for patient: {request.name or request.patient_id}")
        return PatientSearchResult(
            patient_id=request.patient_id or "PT-12345",
            name=request.name or "John Doe",
            dob=request.dob or "1980-01-01",
            gender="M",
            status="ACTIVE",
            found=True
        )

class MedicalTools:
    @staticmethod
    async def lookup_drug(request: DrugLookupRequest) -> DrugLookupResult:
        logger.info(f"Looking up drug: {request.drug_name}")
        # Mock API call to drug database
        if request.drug_name.lower() == "aspirin":
            return DrugLookupResult(
                drug_name="Aspirin",
                active_ingredients=["Acetylsalicylic acid"],
                contraindications=["Bleeding disorders", "Asthma"],
                side_effects=["Stomach upset", "Bleeding"],
                standard_dosage="81mg to 325mg daily",
                found=True
            )
        return DrugLookupResult(
            drug_name=request.drug_name,
            active_ingredients=[], contraindications=[], side_effects=[], standard_dosage="", found=False
        )

    @staticmethod
    async def check_interactions(request: DrugInteractionRequest) -> DrugInteractionResult:
        logger.info(f"Checking interactions for: {request.drugs}")
        drugs = [d.lower() for d in request.drugs]
        if "warfarin" in drugs and "aspirin" in drugs:
            return DrugInteractionResult(
                interactions_found=True,
                warnings=["High risk of bleeding. Concurrent use generally contraindicated."],
                severity="CRITICAL"
            )
        return DrugInteractionResult(interactions_found=False, warnings=[], severity="LOW")

    @staticmethod
    async def calculate_dosage(request: DosageCalculatorRequest) -> DosageCalculatorResult:
        logger.info(f"Calculating dosage for {request.drug_name} for {request.patient_weight_kg}kg patient.")
        dose = request.patient_weight_kg * 5.0 # Mock formula: 5mg / kg
        return DosageCalculatorResult(
            drug_name=request.drug_name,
            recommended_dose=f"{dose}mg",
            max_daily_dose=f"{dose * 3}mg",
            warnings=["Adjust for renal impairment if applicable."]
        )

    @staticmethod
    async def search_icd(request: ICDSearchRequest) -> ICDSearchResult:
        logger.info(f"Searching ICD for: {request.description}")
        return ICDSearchResult(
            matches=[
                {"code": "J01.90", "description": "Acute sinusitis, unspecified"},
                {"code": "J45.909", "description": "Unspecified asthma, uncomplicated"}
            ]
        )

class AdminTools:
    @staticmethod
    async def lookup_insurance(request: InsuranceLookupRequest) -> InsuranceLookupResult:
        logger.info(f"Checking insurance for PT {request.patient_id}, Proc {request.procedure_code}")
        # Mock response
        if request.procedure_code.startswith("E"): # Emergency
             return InsuranceLookupResult(is_covered=True, copay_amount=150.0, authorization_required=False, notes="Emergency waiver applied.")
             
        return InsuranceLookupResult(
            is_covered=True,
            copay_amount=45.0,
            authorization_required=True,
            notes="Requires prior auth for specialist visits."
        )
