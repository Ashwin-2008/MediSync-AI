from .seeder_1_auth_hospital import seed_auth_hospital
from .seeder_2_doctors import seed_doctors
from .seeder_3_patients import seed_patients
from .seeder_4_appointments_vitals import seed_appointments_vitals
from .seeder_5_treatment import seed_treatment
from .seeder_6_labs import seed_labs
from .seeder_7_workflow import seed_workflow
from .seeder_8_conversations import seed_conversations
from .seeder_9_billing import seed_billing
from .seeder_10_analytics import seed_analytics

__all__ = [
    "seed_auth_hospital",
    "seed_doctors",
    "seed_patients",
    "seed_appointments_vitals",
    "seed_treatment",
    "seed_labs",
    "seed_workflow",
    "seed_conversations",
    "seed_billing",
    "seed_analytics"
]
