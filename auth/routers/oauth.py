from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse 
from auth.oauth import get_google_auth_flow, verify_google_token
from core.models import User
from sqlalchemy.orm import Session
from core.dependencies import get_db

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

@router.get("/google/callback", response_class=HTMLResponse)
def callback(code: str, state: str, db: Session = Depends(get_db)):
    """
    Callback после авторизации в Google.
    Закрывает окно после успешной авторизации.
    """
    flow = get_google_auth_flow()
    flow.fetch_token(code=code)

    credentials = flow.credentials
    idinfo = verify_google_token(credentials.id_token)

    if not idinfo:
        raise HTTPException(status_code=400, detail="Invalid token")

    telegram_id = state
    email = idinfo.get("email")

    # Проверяем, существует ли пользователь
    user = db.query(User).filter(User.telegram_id == telegram_id).first()

    if user:
        # Обновляем токены
        user.email = email
        user.google_token = credentials.token
        user.google_refresh_token = credentials.refresh_token
        db.commit()
        db.refresh(user)
    else:
        # Создаем нового пользователя
        user = User(
            telegram_id=telegram_id,
            email=email,
            google_token=credentials.token,
            google_refresh_token=credentials.refresh_token,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Возвращаем HTML для автоматического закрытия окна
    return """
    <html>
        <head>
            <title>Авторизация завершена</title>
        </head>
        <body>
            <script>
                window.opener.postMessage({{status: "success", token: "{access_token}"}}, "*");
                window.close();
            </script>
            <p>Вы успешно авторизовались! Это окно закроется автоматически.</p>
        </body>
    </html>
    """
