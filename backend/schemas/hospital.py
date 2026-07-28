import uuid
from typing import List, Optional
from pydantic import Field
from .base import BaseSchema, UUIDSchema, PaginationSchema

# Setting
class SettingBase(BaseSchema):
    key: str
    value: str
    description: Optional[str] = None
    is_public: bool = False

class SettingCreate(SettingBase):
    pass

class SettingUpdate(BaseSchema):
    value: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

class SettingResponse(SettingBase, UUIDSchema):
    pass

# Hospital
class HospitalBase(BaseSchema):
    name: str
    address: str
    contact_email: str
    contact_phone: str

class HospitalCreate(HospitalBase):
    pass

class HospitalUpdate(BaseSchema):
    name: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

class HospitalResponse(HospitalBase, UUIDSchema):
    pass

# Department
class DepartmentBase(BaseSchema):
    hospital_id: uuid.UUID
    name: str
    description: Optional[str] = None
    head_doctor_id: Optional[uuid.UUID] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    head_doctor_id: Optional[uuid.UUID] = None

class DepartmentResponse(DepartmentBase, UUIDSchema):
    pass

class PaginatedDepartmentResponse(PaginationSchema):
    items: List[DepartmentResponse]

# Room
class RoomBase(BaseSchema):
    department_id: uuid.UUID
    room_number: str
    room_type: str
    capacity: int

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseSchema):
    room_type: Optional[str] = None
    capacity: Optional[int] = None

class RoomResponse(RoomBase, UUIDSchema):
    pass

# Bed
class BedBase(BaseSchema):
    room_id: uuid.UUID
    bed_number: str
    status: str

class BedCreate(BedBase):
    pass

class BedUpdate(BaseSchema):
    status: Optional[str] = None

class BedResponse(BedBase, UUIDSchema):
    pass

# Admission
class AdmissionBase(BaseSchema):
    patient_id: uuid.UUID
    bed_id: uuid.UUID
    admitting_doctor_id: uuid.UUID
    reason_for_admission: str
    status: str = "ADMITTED"

class AdmissionCreate(AdmissionBase):
    pass

class AdmissionUpdate(BaseSchema):
    bed_id: Optional[uuid.UUID] = None
    status: Optional[str] = None

class AdmissionResponse(AdmissionBase, UUIDSchema):
    pass

# Discharge
class DischargeBase(BaseSchema):
    admission_id: uuid.UUID
    discharging_doctor_id: uuid.UUID
    discharge_summary: str
    follow_up_instructions: Optional[str] = None

class DischargeCreate(DischargeBase):
    pass

class DischargeUpdate(BaseSchema):
    discharge_summary: Optional[str] = None
    follow_up_instructions: Optional[str] = None

class DischargeResponse(DischargeBase, UUIDSchema):
    pass
