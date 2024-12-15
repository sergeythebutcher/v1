import os
import logging
import time
from fastapi import HTTPException
from google_auth_oauthlib.flow import Flow
from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport.requests import Request
from dotenv import load_dotenv
from core.models import User
import hashlib
import hmac

# Логирование ошибок
logging.basicConfig(level=logging.INFO)

# Загрузка переменных из .env
load_dotenv()

# Путь к JSON-файлу с настройками клиента
CLIENT_SECRETS_FILE = os.getenv("GOOGLE_CLIENT_SECRETS_FILE")

# Telegram Bot Token для проверки подписи
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Настройка Flow для OAuth
def get_google_auth_flow():
    """
    Инициализация Google OAuth Flow из файла client_secrets.json.
    """
    return Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ],
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI"),
    )

# Проверка токена
def verify_google_token(token):
    """
    Проверяет валидность токена Google ID.
    """
    try:
        time.sleep(2)  # Задержка на 2 секунды перед проверкой
        idinfo = verify_oauth2_token(token, Request())
        if "accounts.google.com" in idinfo["iss"] or "https://accounts.google.com" in idinfo["iss"]:
            return idinfo
        raise ValueError("Wrong issuer.")
    except ValueError as e:
        logging.error(f"Token verification failed: {e}")
        return None

# Проверка токена для пользователя
def check_google_token(user: User):
    """
    Проверяет, действителен ли токен Google для пользователя.
    """
    if not user.google_token:
        logging.warning(f"User ID {user.id} does not have a Google token.")
        raise HTTPException(status_code=401, detail="Google OAuth token is missing.")

    token_info = verify_google_token(user.google_token)
    if not token_info:
        logging.warning(f"Invalid Google token for user ID {user.id}.")
        raise HTTPException(status_code=401, detail="Google OAuth token is invalid.")

    logging.info(f"Google token for user ID {user.id} is valid.")
    return token_info

# Генерация OAuth ссылки
def generate_google_auth_url(telegram_id: str) -> str:
    """
    Генерация Google OAuth URL с использованием get_google_auth_flow.
    """
    flow = get_google_auth_flow()
    auth_url, _ = flow.authorization_url(prompt="consent", state=telegram_id)
    return auth_url

# Проверка подписи Telegram auth_data
def validate_telegram_auth(auth_data: dict):
    """
    Проверяет валидность данных авторизации Telegram, используя токен Telegram Bot.
    """
    data_check_string = "\n".join(
        [f"{key}={auth_data[key]}" for key in sorted(auth_data) if key != "hash"]
    )
    secret_key = hashlib.sha256(TELEGRAM_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if calculated_hash != auth_data.get("hash"):
        logging.error("Invalid Telegram auth data.")
        raise HTTPException(status_code=400, detail="Invalid Telegram auth data.")
    logging.info("Telegram auth data is valid.")
