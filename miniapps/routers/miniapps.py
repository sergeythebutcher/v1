from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from core.dependencies import get_db
from core.models import User, Project
from auth.oauth import get_google_auth_flow, check_google_token
import hashlib
import hmac
import os
import logging

logging.basicConfig(level=logging.INFO)


router = APIRouter()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def validate_telegram_auth(auth_data: dict):
    """
    Валидация подписи auth_data от Telegram.
    """
    try:
        # Убедимся, что есть обязательные поля
        if "hash" not in auth_data or "id" not in auth_data:
            raise ValueError("Missing required auth data fields")

        # Формируем строку data_check_string, исключая 'hash' и 'signature'
        data_check_string = "\n".join(
            f"{key}={auth_data[key]}" for key in sorted(auth_data) if key not in ["hash", "signature"]
        )
        logging.info(f"Data Check String: {data_check_string}")

        # Генерация секретного ключа
        secret_key = hashlib.sha256(TELEGRAM_TOKEN.encode()).digest()

        # Вычисляем хеш
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        logging.info(f"Calculated Hash: {calculated_hash}")
        logging.info(f"Provided Hash: {auth_data.get('hash')}")
        logging.info(f"TELEGRAM_TOKEN: {TELEGRAM_TOKEN}")
        logging.info(f"Received auth_data: {auth_data}")
        logging.info(f"Data Check String: {data_check_string}")



        # Сравниваем вычисленный хеш с предоставленным
        if calculated_hash != auth_data["hash"]:
            raise ValueError("Invalid Telegram auth data")

        # Проверяем срок действия auth_date (допустим 24 часа)
        if time.time() - int(auth_data["auth_date"]) > 86400:
            raise ValueError("Auth date expired")

    except Exception as e:
        logging.error(f"Error in Telegram auth validation: {e}")
        raise HTTPException(status_code=400, detail="Invalid Telegram auth data")




@router.get("/", response_class=HTMLResponse, tags=["MiniApps"])
async def miniapps_home():
    """
    Возвращает HTML-страницу MiniApps.
    """
    with open("miniapps/templates/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@router.post("/validate_user", tags=["MiniApps"])
def validate_user(auth_data: dict, db: Session = Depends(get_db)):
    logging.info(f"Received auth_data: {auth_data}")

    validate_telegram_auth(auth_data)

    telegram_id = auth_data.get("id")
    if not telegram_id:
        raise HTTPException(status_code=400, detail="Missing 'telegram_id'")

    user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()
    if not user:
        flow = get_google_auth_flow()
        auth_url, _ = flow.authorization_url(prompt="consent", state=telegram_id)
        return {"redirect_url": auth_url}

    if not user.google_token or not check_google_token(user.google_token):
        flow = get_google_auth_flow()
        auth_url, _ = flow.authorization_url(prompt="consent", state=telegram_id)
        return {"redirect_url": auth_url}

    projects = db.query(Project).filter(Project.user_id == user.id).all()
    return {"projects": [{"id": p.id, "name": p.name} for p in projects]}
