import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import CRUDBase
from backend.models.hospital import Hospital, Department, Room, Bed, Admission, Discharge
from backend.schemas.hospital import HospitalCreate, HospitalUpdate, DepartmentCreate, DepartmentUpdate, RoomCreate, RoomUpdate, BedCreate, BedUpdate, AdmissionCreate, AdmissionUpdate, DischargeCreate, DischargeUpdate

class CRUDHospital(CRUDBase[Hospital, HospitalCreate, HospitalUpdate]):
    pass

class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    async def get_by_hospital(self, db: AsyncSession, *, hospital_id: uuid.UUID) -> List[Department]:
        result = await db.execute(select(Department).filter(Department.hospital_id == hospital_id))
        return list(result.scalars().all())

class CRUDRoom(CRUDBase[Room, RoomCreate, RoomUpdate]):
    async def get_by_department(self, db: AsyncSession, *, department_id: uuid.UUID) -> List[Room]:
        result = await db.execute(select(Room).filter(Room.department_id == department_id))
        return list(result.scalars().all())

class CRUDBed(CRUDBase[Bed, BedCreate, BedUpdate]):
    async def get_by_room(self, db: AsyncSession, *, room_id: uuid.UUID) -> List[Bed]:
        result = await db.execute(select(Bed).filter(Bed.room_id == room_id))
        return list(result.scalars().all())

class CRUDAdmission(CRUDBase[Admission, AdmissionCreate, AdmissionUpdate]):
    async def get_active_by_patient(self, db: AsyncSession, *, patient_id: uuid.UUID) -> Optional[Admission]:
        result = await db.execute(
            select(Admission)
            .filter(Admission.patient_id == patient_id, Admission.status == "ADMITTED")
        )
        return result.scalars().first()

class CRUDDischarge(CRUDBase[Discharge, DischargeCreate, DischargeUpdate]):
    pass

hospital = CRUDHospital(Hospital)
department = CRUDDepartment(Department)
room = CRUDRoom(Room)
bed = CRUDBed(Bed)
admission = CRUDAdmission(Admission)
discharge = CRUDDischarge(Discharge)
