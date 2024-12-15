from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse
from auth.oauth import get_google_auth_flow, verify_google_token
from core.models import User
from sqlalchemy.orm import Session
from core.dependencies import get_db
from auth.jwt import create_access_token

router = APIRouter()

@router.get("/login")
def login(telegram_id: str = Query(...)):
    """
    Генерация ссылки для входа через Google OAuth.
    Передается telegram_id для связи учетной записи Telegram и Google.
    """
    flow = get_google_auth_flow()
    auth_url, _ = flow.authorization_url(prompt="consent", state=telegram_id)
    return {"auth_url": auth_url}

@router.get("/google/callback")
def callback(code: str, state: str, db: Session = Depends(get_db)):
    """
    Callback после авторизации через Google.
    """
    telegram_id = state  # Извлекаем telegram_id из state
    flow = get_google_auth_flow()
    flow.fetch_token(code=code)

    credentials = flow.credentials
    user = db.query(User).filter(User.telegram_id == telegram_id).first()

    if not user:
        user = User(
            telegram_id=telegram_id,
            email=credentials.id_token.get("email"),
            google_token=credentials.token,
            google_refresh_token=credentials.refresh_token
        )
        db.add(user)
        db.commit()
    else:
        user.google_token = credentials.token
        user.google_refresh_token = credentials.refresh_token
        db.commit()

    return {"message": "Authorization successful"}