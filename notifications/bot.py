import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from core.db import SessionLocal
from core.models import User
from auth.jwt import create_access_token, get_current_user
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
    Регистрация пользователя, проверка OAuth токена и генерация JWT.
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

        # Проверка токенов Google
        if not user.google_token or not verify_google_token(user.google_token):
            # Если токена нет или он недействителен, отправляем ссылку для OAuth
            oauth_url = generate_oauth_url(str(telegram_id))
            await update.message.reply_text(
                f"Для доступа к функционалу пройдите авторизацию Google:\n{oauth_url}"
            )
        else:
            # Если токен Google действителен, создаем JWT
            access_token = create_access_token({"user_id": user.id})
            await update.message.reply_text(
                "У вас уже есть доступ к функционалу Budget Checker.\n"
                f"Ваш JWT токен: {access_token}\n"
                "Используйте его для доступа к API или Mini App."
            )

# Обработчик команды /token
async def get_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Генерация нового JWT токена для авторизованного пользователя.
    """
    telegram_id = update.message.chat.id

    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()
        if not user or not verify_google_token(user.google_token):
            # Если пользователь не авторизован
            await update.message.reply_text(
                "Вы не авторизованы. Пройдите авторизацию через Google сначала."
            )
        else:
            # Генерация нового JWT токена
            access_token = create_access_token({"user_id": user.id})
            await update.message.reply_text(
                f"Ваш JWT токен: {access_token}\n"
                "Используйте его для доступа к API или Mini App."
            )

# Регистрация обработчиков команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("token", get_token))

# Запуск бота
if __name__ == "__main__":
    print("Telegram Bot запущен...")
    application.run_polling()
