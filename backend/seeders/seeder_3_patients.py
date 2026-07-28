import uuid
from backend.seed_utils import fake, generate_uuid, bulk_insert, generate_indian_phone, INSURANCE_PROVIDERS
from backend.models.patient import Patient, PatientProfile, PatientAddress, EmergencyContact, InsurancePolicy

async def seed_patients(db, config, context, batch_size):
    patients = []
    profiles = []
    addresses = []
    contacts = []
    insurances = []
    patient_ids = []
    
    for _ in range(config["patients"]):
        patient_id = generate_uuid()
        patient_ids.append(patient_id)
        
        patients.append({
            "id": patient_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": fake.date_of_birth(minimum_age=1, maximum_age=90),
            "gender": fake.random_element(["M", "F", "O"]),
            "email": fake.email(),
            "phone": generate_indian_phone()
        })
        
        profiles.append({
            "id": generate_uuid(),
            "patient_id": patient_id,
            "blood_type": fake.random_element(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
            "marital_status": fake.random_element(["Single", "Married", "Divorced", "Widowed"]),
            "occupation": fake.job()
        })
        
        addresses.append({
            "id": generate_uuid(),
            "patient_id": patient_id,
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.postcode(),
            "country": "India"
        })
        
        # 1-2 Emergency Contacts
        for _ in range(fake.random_int(1, 2)):
            contacts.append({
                "id": generate_uuid(),
                "patient_id": patient_id,
                "name": fake.name(),
                "relationship": fake.random_element(["Spouse", "Parent", "Child", "Sibling", "Friend"]),
                "phone": generate_indian_phone()
            })
            
    # Insurance for about 70% of patients
    insured_patients = fake.random_elements(elements=patient_ids, length=config["insurance_policies"], unique=True)
    for p_id in insured_patients:
        insurances.append({
            "id": generate_uuid(),
            "patient_id": p_id,
            "provider_name": fake.random_element(INSURANCE_PROVIDERS),
            "policy_number": fake.bban(),
            "valid_from": fake.date_this_decade()
        })

    await bulk_insert(db, Patient, patients, batch_size)
    await bulk_insert(db, PatientProfile, profiles, batch_size)
    await bulk_insert(db, PatientAddress, addresses, batch_size)
    await bulk_insert(db, EmergencyContact, contacts, batch_size)
    await bulk_insert(db, InsurancePolicy, insurances, batch_size)
    
    context["patients"] = patient_ids
    return context
