import uuid
from backend.seed_utils import fake, generate_uuid, bulk_insert, DEPARTMENTS, MEDICINES
from backend.models.auth import Role, User
from backend.models.hospital import Hospital, Department, Room, Bed
from backend.models.treatment import Medicine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_auth_hospital(db, config, batch_size):
    context = {}
    
    # 1. Hospital
    hospitals = [{
        "id": generate_uuid(),
        "name": fake.company() + " Hospital",
        "address": fake.address(),
        "contact_email": fake.company_email(),
        "contact_phone": fake.phone_number()
    } for _ in range(config["hospital"])]
    await bulk_insert(db, Hospital, hospitals, batch_size)
    hospital_id = hospitals[0]["id"]
    context["hospital_id"] = hospital_id
    
    # 2. Roles
    roles = [
        {"id": generate_uuid(), "name": "Admin"},
        {"id": generate_uuid(), "name": "Doctor"},
        {"id": generate_uuid(), "name": "Nurse"},
        {"id": generate_uuid(), "name": "Patient"},
        {"id": generate_uuid(), "name": "Receptionist"}
    ]
    await bulk_insert(db, Role, roles, batch_size)
    context["roles"] = {r["name"]: r["id"] for r in roles}
    
    # 3. Users (Admins and Receptionists)
    hashed_password = pwd_context.hash("password123")
    users = []
    
    # Admins
    for _ in range(config["admins"]):
        users.append({
            "id": generate_uuid(),
            "email": fake.email(),
            "username": fake.user_name(),
            "hashed_password": hashed_password,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "role_id": context["roles"]["Admin"]
        })
        
    # Receptionists
    for _ in range(config["receptionists"]):
        users.append({
            "id": generate_uuid(),
            "email": fake.email(),
            "username": fake.user_name(),
            "hashed_password": hashed_password,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "role_id": context["roles"]["Receptionist"]
        })
        
    await bulk_insert(db, User, users, batch_size)
    
    # 4. Departments
    dept_data = []
    for d_name in DEPARTMENTS[:config["departments"]]:
        dept_data.append({
            "id": generate_uuid(),
            "hospital_id": hospital_id,
            "name": d_name,
            "description": fake.text(max_nb_chars=100)
        })
    await bulk_insert(db, Department, dept_data, batch_size)
    context["departments"] = [d["id"] for d in dept_data]
    
    # 5. Rooms & Beds
    rooms = []
    beds = []
    for dept_id in context["departments"]:
        for i in range(10): # 10 rooms per department
            room_id = generate_uuid()
            rooms.append({
                "id": room_id,
                "department_id": dept_id,
                "room_number": f"{fake.random_int(1, 9)}{i:02d}",
                "room_type": fake.random_element(["ICU", "General", "Private", "Operation Theater"]),
                "capacity": 4
            })
            for b in range(4): # 4 beds per room
                beds.append({
                    "id": generate_uuid(),
                    "room_id": room_id,
                    "bed_number": f"B{b+1}",
                    "status": "AVAILABLE"
                })
    await bulk_insert(db, Room, rooms, batch_size)
    await bulk_insert(db, Bed, beds, batch_size)
    context["beds"] = [b["id"] for b in beds]
    
    # 6. Medicines
    meds = []
    for i in range(config["medicines"]):
        med_template = MEDICINES[i % len(MEDICINES)]
        meds.append({
            "id": generate_uuid(),
            "name": med_template["name"] + f" (Variant {i})",
            "generic_name": med_template["generic_name"],
            "manufacturer": med_template["manufacturer"],
            "unit_price": med_template["price"] + fake.random_int(-5, 10),
            "stock_quantity": fake.random_int(100, 5000)
        })
    await bulk_insert(db, Medicine, meds, batch_size)
    context["medicines"] = [m["id"] for m in meds]
    
    return context
