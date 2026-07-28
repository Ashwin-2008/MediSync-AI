from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# =======================
# Patient Tools
# =======================
class PatientSearchRequest(BaseModel):
    name: Optional[str] = None
    dob: Optional[str] = None
    patient_id: Optional[str] = None

class PatientSearchResult(BaseModel):
    patient_id: str
    name: str
    dob: str
    gender: str
    status: str
    found: bool

# =======================
# Medical Tools
# =======================
class DrugLookupRequest(BaseModel):
    drug_name: str
    
class DrugLookupResult(BaseModel):
    drug_name: str
    active_ingredients: List[str]
    contraindications: List[str]
    side_effects: List[str]
    standard_dosage: str
    found: bool

class DrugInteractionRequest(BaseModel):
    drugs: List[str]

class DrugInteractionResult(BaseModel):
    interactions_found: bool
    warnings: List[str]
    severity: str = Field(description="LOW, MEDIUM, HIGH, CRITICAL")

class DosageCalculatorRequest(BaseModel):
    drug_name: str
    patient_weight_kg: float
    patient_age_years: float
    
class DosageCalculatorResult(BaseModel):
    drug_name: str
    recommended_dose: str
    max_daily_dose: str
    warnings: List[str]

class ICDSearchRequest(BaseModel):
    description: str

class ICDSearchResult(BaseModel):
    matches: List[Dict[str, str]] = Field(description="List of dicts with 'code' and 'description'")

# =======================
# Admin Tools
# =======================
class InsuranceLookupRequest(BaseModel):
    patient_id: str
    procedure_code: str
    
class InsuranceLookupResult(BaseModel):
    is_covered: bool
    copay_amount: float
    authorization_required: bool
    notes: str
