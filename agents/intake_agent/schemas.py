from pydantic import BaseModel, Field
from typing import Optional, List

class PatientIntakeInput(BaseModel):
    patient_id: Optional[str] = None
    first_name: str
    last_name: str
    age: int
    gender: str
    symptoms: List[str]
    duration_days: int
    notes: Optional[str] = None

class PatientIntakeOutput(BaseModel):
    patient_id: str
    triage_level: str = Field(..., description="1-5 triage level (1=Resuscitation, 5=Non-urgent)")
    recommended_department: str
    summary: str
    next_state: str = "INTAKE_COMPLETE"
