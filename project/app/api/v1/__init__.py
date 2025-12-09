from fastapi import APIRouter
from .clients import router as clients_router
from .vehicles import api_router as vehicles_router
from .parking import api_router as parking_spaces_router
from .tariffs import api_router as tariffs_router
from .parking_sessions import api_router as parking_sessions_router
from .payments import api_router as payments_router
from .references import api_router as references_router
from .reports import api_router as reports_router

api_router = APIRouter()

api_router.include_router(clients_router)
api_router.include_router(vehicles_router)
api_router.include_router(parking_spaces_router)
api_router.include_router(tariffs_router)
api_router.include_router(parking_sessions_router)
api_router.include_router(payments_router)
api_router.include_router(references_router)
api_router.include_router(reports_router)
