budget_checker/
├── auth/                      # Подсервис для аутентификации и OAuth
│   ├── __init__.py
│   ├── oauth.py               # Логика OAuth для Google и Facebook
│   ├── routers/
│   │   ├── __init__.py
│   │   └── oauth.py           # Роутинг для авторизации
├── projects/                  # Подсервис для работы с проектами
│   ├── __init__.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── projects.py        # Роутинг для проектов
│   │   └── ad_accounts.py     # Роутинг для рекламных кабинетов
│   ├── crud.py                # CRUD-операции для проектов и кабинетов
├── notifications/             # Подсервис для уведомлений
│   ├── __init__.py
│   ├── telegram/
│   │   ├── __init__.py
│   │   ├── bot.py             # Telegram Bot API
│   │   ├── miniapps.py        # Telegram Mini Apps логика
│   │   └── handlers.py        # Обработчики событий Telegram
├── tasks/                     # Подсервис для фоновых задач
│   ├── __init__.py
│   ├── celery_config.py       # Конфигурация Celery
│   ├── periodic.py            # Периодические задачи
│   └── notifications.py       # Задачи для отправки уведомлений
├── core/                      # Общие компоненты
│   ├── __init__.py
│   ├── main.py                # Основное приложение FastAPI
│   ├── models.py              # SQLAlchemy модели
│   ├── db.py                  # Подключение к базе данных
│   ├── dependencies.py        # Общие зависимости
│   ├── service_config.py      # Глобальные настройки сервиса
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


1. Подсервис auth
    Назначение: Работа с аутентификацией и OAuth.
    Функции:
    Авторизация через Google и Facebook.
    Сохранение и обновление токенов в базе.
    Ключевые файлы:
    oauth.py: Логика работы с OAuth.
    routers/oauth.py: Роутинг для авторизации.
2. Подсервис projects
    Назначение: Управление проектами и рекламными кабинетами.
    Функции:
    Создание, просмотр, обновление и удаление проектов.
    Привязка рекламных кабинетов к проектам.
    Ключевые файлы:
    routers/projects.py: Роутинг для проектов.
    routers/ad_accounts.py: Роутинг для рекламных кабинетов.
    crud.py: CRUD-операции.
3. Подсервис notifications
    Назначение: Уведомления через Telegram.
    Функции:
    Работа с Telegram Bot API.
    Реализация Telegram Mini Apps.
    Обработка событий и отправка уведомлений пользователям.
    Ключевые файлы:
    telegram/bot.py: Логика Telegram Bot.
    telegram/miniapps.py: Логика Mini Apps.
    telegram/handlers.py: Обработчики Telegram.
4. Подсервис tasks
    Назначение: Выполнение фоновых задач.
    Функции:
    Настройка Celery.
    Выполнение периодических задач (например, обновление данных рекламы).
    Отправка уведомлений.
    Ключевые файлы:
    celery_config.py: Конфигурация Celery.
    periodic.py: Периодические задачи.
    notifications.py: Логика задач уведомлений.
5. Подсервис core
    Назначение: Общие компоненты и конфигурация сервиса.
    Функции:
    Модели базы данных.
    Подключение к базе данных.
    Зависимости для маршрутов.
    Глобальные настройки.
    Ключевые файлы:
    main.py: Запуск FastAPI приложения.
    models.py: Модели SQLAlchemy.
    db.py: Подключение к базе данных.
    dependencies.py: Зависимости.
    service_config.py: Глобальные настройки.





    # Budget Checker

Budget Checker — это сервис для управления проектами и рекламными кампаниями через Telegram Mini Apps и веб-интерфейс. Проект использует FastAPI, Celery и интеграции с Google Ads и Facebook Ads.

## Установка и запуск

### 1. Установите Docker и Docker Compose
Убедитесь, что на вашей машине установлены [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/).

### 2. Клонируйте репозиторий
```bash
git clone https://github.com/your-repo/budget_checker.git
cd budget_checker