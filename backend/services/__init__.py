from .patient_service import PatientService
from .doctor_service import DoctorService
from .appointment_service import AppointmentService
from .workflow_service import WorkflowService

# Easy access to get services
def get_patient_service(db) -> PatientService:
    return PatientService(db)

def get_doctor_service(db) -> DoctorService:
    return DoctorService(db)

def get_appointment_service(db) -> AppointmentService:
    return AppointmentService(db)

def get_workflow_service(db) -> WorkflowService:
    return WorkflowService(db)
