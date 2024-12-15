import os
from fastapi.responses import HTMLResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import logging
import time


# Логирование ошибок
logging.basicConfig(level=logging.INFO)


# Путь к JSON-файлу с настройками клиента
CLIENT_SECRETS_FILE = os.getenv("GOOGLE_CLIENT_SECRETS_FILE")
# Загрузка переменных из .env
load_dotenv()
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