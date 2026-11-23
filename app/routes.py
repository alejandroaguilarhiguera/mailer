from fastapi import APIRouter

from app.routers.health import router as health_router
from app.routers.mail_router import router as mail_router
api_router = APIRouter()

# Registrar cada router individual
api_router.include_router(health_router)
api_router.include_router(mail_router)
