from fastapi import APIRouter
from notifications.miniapps import router as miniapps_router

router = APIRouter()

# Подключение маршрутов Mini Apps
router.include_router(miniapps_router, prefix="/miniapps", tags=["Mini Apps"])
