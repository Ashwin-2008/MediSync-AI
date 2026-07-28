from fastapi import APIRouter

from .auth import router as auth_router
from .patients import router as patients_router
from .doctors import router as doctors_router
from .appointments import router as appointments_router
from .treatments import router as treatments_router
from .labs import router as labs_router
from .billing import router as billing_router
from .insurance import router as insurance_router
from .notifications import router as notifications_router
from .workflow import router as workflow_router
from .conversation import router as conversation_router
from .analytics import router as analytics_router
from .settings import router as settings_router
from .admin import router as admin_router

__all__ = [
    "auth_router",
    "patients_router",
    "doctors_router",
    "appointments_router",
    "treatments_router",
    "labs_router",
    "billing_router",
    "insurance_router",
    "notifications_router",
    "workflow_router",
    "conversation_router",
    "analytics_router",
    "settings_router",
    "admin_router"
]
