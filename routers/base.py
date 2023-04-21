from fastapi import APIRouter
from routers.addresses import address_router

api_router = APIRouter()

api_router.include_router(address_router, prefix="/api_v1", tags=["Addresses"])

