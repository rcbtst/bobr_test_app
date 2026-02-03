from fastapi import APIRouter, FastAPI

from src.interfaces.rest_api.routes.tasks import router as tasks_router

health_router = APIRouter(prefix="/health", include_in_schema=False)


@health_router.get("")
async def health_check():
    return {"health": "OK"}


def setup_routes(app: FastAPI):
    app.include_router(health_router)
    app.include_router(tasks_router)
