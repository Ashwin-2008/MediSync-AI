import uuid
from backend.seed_utils import fake, generate_uuid, bulk_insert, SPECIALIZATIONS
from backend.models.auth import User
from backend.models.clinical import Doctor, DoctorSchedule
from passlib.context import CryptContext
from datetime import time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_doctors(db, config, context, batch_size):
    hashed_password = pwd_context.hash("password123")
    
    doctors = []
    users = []
    doctor_ids = []
    
    for i in range(config["doctors"]):
        user_id = generate_uuid()
        doctor_id = generate_uuid()
        email = "doctor@hospital.com" if i == 0 else fake.email()
        username = "doctor" if i == 0 else fake.user_name()
        first_name = "Doctor" if i == 0 else fake.first_name()
        last_name = "User" if i == 0 else fake.last_name()
        
        users.append({
            "id": user_id,
            "email": email,
            "username": username,
            "hashed_password": hashed_password,
            "first_name": first_name,
            "last_name": last_name,
            "role_id": context["roles"]["Doctor"]
        })
        
        doctors.append({
            "id": doctor_id,
            "user_id": user_id,
            "department_id": fake.random_element(context["departments"]),
            "specialization": fake.random_element(SPECIALIZATIONS),
            "license_number": f"LIC-{fake.random_int(10000, 99999)}",
            "years_of_experience": fake.random_int(2, 35)
        })
        doctor_ids.append(doctor_id)
        
    await bulk_insert(db, User, users, batch_size)
    await bulk_insert(db, Doctor, doctors, batch_size)
    
    schedules = []
    for doc_id in doctor_ids:
        # Give each doctor a schedule for Mon-Fri (0-4)
        for day in range(5):
            schedules.append({
                "id": generate_uuid(),
                "doctor_id": doc_id,
                "day_of_week": day,
                "start_time": time(9, 0),
                "end_time": time(17, 0)
            })
            
    await bulk_insert(db, DoctorSchedule, schedules, batch_size)
    context["doctors"] = doctor_ids
    return context
