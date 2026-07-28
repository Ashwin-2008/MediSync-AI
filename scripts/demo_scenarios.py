# Pre-packaged JSON scenarios for instant API testing/demonstrations

CHEST_PAIN_SCENARIO = {
    "workflow_type": "EMERGENCY_ADMISSION",
    "patient_id": "PT-12345",
    "symptoms": ["Severe crushing chest pain", "Radiating to left arm", "Diaphoresis", "Shortness of breath"],
    "vitals": {
        "heart_rate": 115,
        "blood_pressure": "160/95",
        "spo2": 94,
        "temperature": 37.1
    },
    "allergies": ["Penicillin"]
}

PNEUMONIA_DRUG_ALLERGY_SCENARIO = {
    "workflow_type": "INPATIENT_ADMISSION",
    "patient_id": "PT-99887",
    "symptoms": ["Productive cough", "High fever", "Chills"],
    "vitals": {
        "heart_rate": 105,
        "blood_pressure": "110/70",
        "spo2": 91,
        "temperature": 39.4,
        "respiratory_rate": 28
    },
    "history": ["Asthma"],
    # The safety engine should catch this prescribing error
    "proposed_treatment": ["Amoxicillin 500mg"],
    "allergies": ["Amoxicillin"] 
}

DIABETES_FOLLOWUP_SCENARIO = {
    "workflow_type": "OUTPATIENT_FOLLOWUP",
    "patient_id": "PT-44556",
    "symptoms": ["Increased thirst", "Fatigue"],
    "labs": [
        {"test": "HbA1c", "value": "8.5%", "status": "High"}
    ],
    "current_medications": ["Metformin 500mg BID"]
}

SCENARIOS = {
    "chest_pain": CHEST_PAIN_SCENARIO,
    "pneumonia_allergy": PNEUMONIA_DRUG_ALLERGY_SCENARIO,
    "diabetes_followup": DIABETES_FOLLOWUP_SCENARIO
}
