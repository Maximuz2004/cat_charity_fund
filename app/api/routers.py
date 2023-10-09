from fastapi import APIRouter

from app.api.endpoints import charity_project_router, user_router

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(charity_project_router)
