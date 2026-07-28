import random
import uuid
from faker import Faker
from datetime import timedelta

fake = Faker('en_IN')

# Indian context Medical lists
DEPARTMENTS = ["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Oncology", "General Surgery", "Gynecology", "Dermatology", "Psychiatry", "Radiology", "Emergency", "Internal Medicine", "Gastroenterology", "Urology", "Endocrinology"]

SPECIALIZATIONS = ["Cardiologist", "Neurologist", "Orthopedic Surgeon", "Pediatrician", "Oncologist", "General Surgeon", "Gynecologist", "Dermatologist", "Psychiatrist", "Radiologist", "Emergency Physician", "Physician", "Gastroenterologist", "Urologist", "Endocrinologist"]

MEDICINES = [
    {"name": "Paracetamol 500mg", "generic_name": "Acetaminophen", "manufacturer": "Cipla", "price": 25.0},
    {"name": "Amoxicillin 250mg", "generic_name": "Amoxicillin", "manufacturer": "Sun Pharma", "price": 45.0},
    {"name": "Amlodipine 5mg", "generic_name": "Amlodipine", "manufacturer": "Dr. Reddy's", "price": 30.0},
    {"name": "Metformin 500mg", "generic_name": "Metformin", "manufacturer": "Lupin", "price": 20.0},
    {"name": "Omeprazole 20mg", "generic_name": "Omeprazole", "manufacturer": "Torrent Pharma", "price": 35.0},
    {"name": "Atorvastatin 10mg", "generic_name": "Atorvastatin", "manufacturer": "Zydus Cadila", "price": 40.0},
    {"name": "Losartan 50mg", "generic_name": "Losartan", "manufacturer": "Aurobindo", "price": 28.0},
    {"name": "Azithromycin 500mg", "generic_name": "Azithromycin", "manufacturer": "Mankind", "price": 50.0},
    {"name": "Pantoprazole 40mg", "generic_name": "Pantoprazole", "manufacturer": "Alkem", "price": 38.0},
    {"name": "Ibuprofen 400mg", "generic_name": "Ibuprofen", "manufacturer": "Abbott India", "price": 22.0},
]

ICD10_CODES = {
    "J00": "Acute nasopharyngitis [common cold]",
    "I10": "Essential (primary) hypertension",
    "E11.9": "Type 2 diabetes mellitus without complications",
    "J45.909": "Unspecified asthma, uncomplicated",
    "M54.5": "Low back pain",
    "J02.9": "Acute pharyngitis, unspecified",
    "R51": "Headache",
    "K21.9": "Gastro-esophageal reflux disease without esophagitis",
    "E78.5": "Hyperlipidemia, unspecified",
    "M17.9": "Osteoarthritis of knee, unspecified"
}

SYMPTOMS = ["Fever", "Cough", "Headache", "Fatigue", "Nausea", "Shortness of breath", "Chest pain", "Abdominal pain", "Joint pain", "Dizziness"]

LAB_TESTS = [
    {"name": "Complete Blood Count (CBC)", "parameter": "Hemoglobin", "unit": "g/dL", "ref": "12.0 - 15.5"},
    {"name": "Lipid Profile", "parameter": "Total Cholesterol", "unit": "mg/dL", "ref": "< 200"},
    {"name": "Blood Glucose Fasting", "parameter": "Glucose", "unit": "mg/dL", "ref": "70 - 100"},
    {"name": "Liver Function Test", "parameter": "ALT", "unit": "U/L", "ref": "7 - 56"},
    {"name": "Thyroid Profile", "parameter": "TSH", "unit": "mIU/L", "ref": "0.4 - 4.0"},
]

INSURANCE_PROVIDERS = ["Star Health", "HDFC ERGO", "ICICI Lombard", "Niva Bupa", "Care Health Insurance", "New India Assurance"]

def generate_uuid():
    return uuid.uuid4()

def generate_indian_phone():
    return f"+91-{fake.random_int(min=6000000000, max=9999999999)}"

def random_date_between(start_date, end_date):
    return fake.date_time_between(start_date=start_date, end_date=end_date)

def get_random_medicine():
    return random.choice(MEDICINES)

def get_random_icd10():
    code = random.choice(list(ICD10_CODES.keys()))
    return code, ICD10_CODES[code]

def get_random_lab_test():
    return random.choice(LAB_TESTS)

async def bulk_insert(db_session, model, data_list, batch_size=5000):
    """
    Efficient bulk insert using SQLAlchemy Core
    """
    from sqlalchemy import insert
    for i in range(0, len(data_list), batch_size):
        batch = data_list[i:i+batch_size]
        await db_session.execute(insert(model).values(batch))
    await db_session.commit()
