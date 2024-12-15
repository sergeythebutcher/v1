import os
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from notifications.handlers.registration import handle_registration
from core.db import SessionLocal
from core.models import User

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start. Запускает регистрацию пользователя.
    """
    await handle_registration(update, context)

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /help. Выводит список доступных команд.
    """
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - Зарегистрироваться\n"
        "/help - Список команд\n"
    )

# Регистрация команд
application.add_handler(CommandHandler("start", start_command))
application.add_handler(CommandHandler("help", help_command))

# Запуск бота
if __name__ == "__main__":
    print("Telegram Bot запущен...")
    application.run_polling()
