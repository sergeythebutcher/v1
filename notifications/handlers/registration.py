from telegram import Update
from telegram.ext import ContextTypes
from core.db import SessionLocal
from core.models import User

async def handle_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработка регистрации пользователя через Telegram.
    """
    telegram_id = update.message.chat.id
    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()
        if not user:
            user = User(telegram_id=str(telegram_id))
            db.add(user)
            db.commit()
            await update.message.reply_text("Регистрация завершена! Добро пожаловать!")
        else:
            await update.message.reply_text("Вы уже зарегистрированы! Добро пожаловать обратно!")
