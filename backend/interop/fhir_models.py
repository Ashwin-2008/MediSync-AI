from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class FHIRIdentifier(BaseModel):
    system: Optional[str] = None
    value: str

class FHIRHumanName(BaseModel):
    family: Optional[str] = None
    given: Optional[List[str]] = None

class FHIRPatient(BaseModel):
    resourceType: str = Field(default="Patient")
    id: str
    identifier: Optional[List[FHIRIdentifier]] = None
    name: Optional[List[FHIRHumanName]] = None
    gender: Optional[str] = None
    birthDate: Optional[str] = None

class FHIRCodeableConcept(BaseModel):
    coding: List[Dict[str, str]]
    text: Optional[str] = None

class FHIRCondition(BaseModel):
    resourceType: str = Field(default="Condition")
    id: str
    clinicalStatus: Optional[FHIRCodeableConcept] = None
    verificationStatus: Optional[FHIRCodeableConcept] = None
    code: FHIRCodeableConcept
    subject: Dict[str, str] = Field(description="Reference to Patient")

class FHIRMedicationRequest(BaseModel):
    resourceType: str = Field(default="MedicationRequest")
    id: str
    status: str
    intent: str
    medicationCodeableConcept: FHIRCodeableConcept
    subject: Dict[str, str]

class FHIRObservation(BaseModel):
    resourceType: str = Field(default="Observation")
    id: str
    status: str
    code: FHIRCodeableConcept
    subject: Dict[str, str]
    valueQuantity: Optional[Dict[str, Any]] = None
