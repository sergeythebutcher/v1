from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def telegram_webhook():
    """
    Точка входа для обработки вебхуков Telegram.
    """
    return {"message": "Telegram Webhook endpoint"}

@router.get("/health")
def health_check():
    """
    Проверка работоспособности Telegram роутера.
    """
    return {"status": "ok"}
