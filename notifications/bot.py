import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from core.db import SessionLocal
from core.models import User
from auth.oauth import get_google_auth_flow, verify_google_token


# Получение токена из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Создание бота и приложения Telegram
bot = Bot(token=TELEGRAM_TOKEN)
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Функция генерации ссылки для OAuth авторизации
def generate_oauth_url(telegram_id: str) -> str:
    """
    Генерация OAuth ссылки для авторизации пользователя.
    """
    flow = get_google_auth_flow()
    auth_url, _ = flow.authorization_url(prompt="consent", state=telegram_id)
    return auth_url

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Регистрация пользователя и проверка OAuth токена.
    """
    telegram_id = update.message.chat.id
    first_name = update.message.chat.first_name

    with SessionLocal() as db:
        # Проверяем, существует ли пользователь
        user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()
        if not user:
            # Регистрация нового пользователя
            user = User(
                telegram_id=str(telegram_id),
                email=None,  # Email добавляется позже через OAuth
                google_token=None,
                google_refresh_token=None
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            await update.message.reply_text(
                f"Добро пожаловать, {first_name}! Вы успешно зарегистрированы."
            )
        else:
            await update.message.reply_text(
                f"Добро пожаловать обратно, {first_name}!"
            )
        
        # Проверка токенов
        if not user.google_token or not verify_google_token(user.google_token):
            # Если токена нет или он недействителен, отправляем ссылку для OAuth
            oauth_url = generate_oauth_url(str(telegram_id))
            await update.message.reply_text(
                f"Для доступа к функционалу пройдите авторизацию Google:\n{oauth_url}"
            )
        else:
            # Если токен действителен
            await update.message.reply_text(
                "У вас уже есть доступ к функционалу Budget Checker. Вы можете управлять своими проектами через Mini App."
            )

# Регистрация обработчика команды /start
application.add_handler(CommandHandler("start", start))

# Запуск бота
if __name__ == "__main__":
    print("Telegram Bot запущен...")
    application.run_polling()
