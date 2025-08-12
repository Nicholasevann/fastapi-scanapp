from fastapi import APIRouter
from app.api.endpoints import auth, user,scan

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(scan.router, prefix="/scan", tags=["scan"])