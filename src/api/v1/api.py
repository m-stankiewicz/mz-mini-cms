from fastapi import APIRouter
from .endpoints import domains

api_router = APIRouter()
api_router.include_router(domains.router, prefix="/domains", tags=["domains"])
