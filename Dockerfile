# Используем Python 3.11 как базовый образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY ./requirements.txt /app/requirements.txt
COPY ./auth/client_secrets.json /app/auth/client_secrets.json

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем исходный код проекта
COPY . /app

# Устанавливаем переменную PYTHONPATH для корректных путей импорта
ENV PYTHONPATH=/app

# Экспонируем порт для FastAPI
EXPOSE 8000

# Команда для запуска FastAPI
CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000"]
