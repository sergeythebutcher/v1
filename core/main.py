from fastapi import FastAPI
from core.service_config import SERVICE_CONFIG
from core.db import engine, Base
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError
from auth.routers import oauth
from projects.routers import projects, ad_accounts, operation_periods, budgets
from notifications.routers import router as telegram_router
from miniapps.routers.miniapps import router as miniapps_router

# Инициализация приложения FastAPI
app = FastAPI(
    title="Budget Checker",
    description="API for managing projects, ad campaigns, and providing notifications.",
    version="1.0.0",
)

# Главная страница
@app.get("/")
def root():
    return {"message": "Welcome to Budget Checker!"}

# Проверка конфигурации сервиса
@app.get("/config/")
def get_config():
    return {"allow_new_user_registration": SERVICE_CONFIG["allow_new_user_registration"]}

# Проверка подключения к базе данных
@app.get("/check_db/")
def check_db():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "Database connection successful"}
    except OperationalError as e:
        return {"status": "Database connection failed", "error": str(e)}

# Событие запуска приложения
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

# Подключение маршрутов
app.include_router(oauth.router, prefix="/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(ad_accounts.router, prefix="/ad_accounts", tags=["Ad Accounts"])
app.include_router(operation_periods.router, prefix="/operation_periods", tags=["Operation Periods"])
app.include_router(budgets.router, prefix="/budgets", tags=["Budgets"])
app.include_router(telegram_router, prefix="/telegram", tags=["Telegram"])
app.include_router(miniapps_router, prefix="/miniapps", tags=["MiniApps"])
