# telegram-mini-app-template

Готовый к использованию стартовый набор для Telegram Mini Apps: кабинеты рефералов, SaaS-панели, формы заявок, магазины, личные кабинеты и MVP.

## Стек технологий

- Frontend: React, TypeScript, Vite, Telegram WebApp SDK, CSS с переменными темы Telegram
- Backend: FastAPI, Python 3.12, Pydantic v2, async SQLAlchemy 2.x
- База данных: PostgreSQL
- Миграции: Alembic
- Авторизация: валидация `initData` Telegram WebApp на бэкенде
- API: REST JSON
- Разработка и развертывание: Docker Compose, nginx
- Тесты: pytest

## Быстрый старт

```bash
cp .env.example .env
make up
make migrate
```

После запуска:

- Frontend: http://localhost
- Состояние бэкенда: http://localhost/api/health
- API внутри сети Docker: `http://backend:8000`

Установите настоящий `TELEGRAM_BOT_TOKEN` в `.env` перед тестированием авторизации Telegram.

## Окружение

`.env.example` содержит все необходимые переменные:

```env
PROJECT_NAME=telegram-mini-app-template
ENVIRONMENT=local
DEBUG=true
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost
POSTGRES_DB=telegram_app
POSTGRES_USER=telegram_app
POSTGRES_PASSWORD=telegram_app
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+psycopg://telegram_app:telegram_app@db:5432/telegram_app
TELEGRAM_BOT_TOKEN=change-me
FRONTEND_URL=http://localhost:5173
VITE_API_BASE_URL=/api
```

Никогда не передавайте `TELEGRAM_BOT_TOKEN` на фронтенд. Фронтенд отправляет только `initData` Telegram; бэкенд проверяет их с помощью токена бота.

## Настройка Telegram-бота

1. Откройте `@BotFather` в Telegram.
2. Запустите `/newbot` и скопируйте токен бота в `.env`.
3. Запустите `/setmenubutton` или `/newapp` в зависимости от вашего процесса в BotFather.
4. Установите URL Mini App на ваш HTTPS URL.
5. Для локального тестирования пробросьте nginx с помощью туннеля:

```bash
ngrok http 80
```

или:

```bash
cloudflared tunnel --url http://localhost
```

Используйте сгенерированный HTTPS URL в BotFather. Telegram Mini Apps требуют HTTPS, за исключением некоторых случаев локальной разработки.

Дополнительные команды бота:

```bash
python scripts/create_bot_commands.py --token "$TELEGRAM_BOT_TOKEN"
```

## Как работает авторизация

Фронтенд считывает `window.Telegram.WebApp.initData` и отправляет его:

- `POST /api/auth/telegram` во время первоначального входа
- `GET /api/users/me` через заголовок `X-Telegram-Init-Data`

Бэкенд:

1. Разбирает строку запроса.
2. Извлекает и удаляет `hash`.
3. Создает `data_check_string` из отсортированных пар ключ-значение.
4. Вычисляет HMAC-SHA256 хеш Telegram, используя токен бота.
5. Отклоняет неверные или просроченные `initData` с ошибкой `401`.
6. Создает или обновляет пользователя в PostgreSQL.

`auth_date` по умолчанию ограничен 24 часами.

## API

- `GET /api/health` возвращает `{ "status": "ok" }`
- `POST /api/auth/telegram` принимает `{ "init_data": "..." }`
- `GET /api/users/me` требует заголовок `X-Telegram-Init-Data`

## Команды Make

```bash
make up              # собрать и запустить все сервисы
make down            # остановить сервисы
make logs            # следить за логами
make backend-shell   # оболочка (shell) в контейнере бэкенда
make frontend-shell  # оболочка (shell) в контейнере фронтенда
make migrate         # alembic upgrade head
make makemigration m="сообщение"
make test            # pytest в контейнере бэкенда
make lint            # ruff и eslint
make format          # ruff format и prettier
```

## Структура проекта

```text
backend/     Приложение FastAPI, модели SQLAlchemy, Alembic, pytest
frontend/    React + TypeScript + Vite Telegram Mini App, Nginx
scripts/     Вспомогательные скрипты
.github/     Workflow CI
```

## Развертывание на VPS

1. Установите Docker и Docker Compose.
2. Клонируйте репозиторий.
3. Создайте `.env` из `.env.example`.
4. Установите `TELEGRAM_BOT_TOKEN`, пароль базы данных и публичный `FRONTEND_URL`.
5. (Опционально) Измените `APP_PORT` в `.env`, если порт 80 уже занят на хосте.
6. **Настройка SSL / HTTPS**:
   - **Вариант А: Nginx на хосте** (уже запущен на сервере). Установите `APP_PORT` (например, 8000) и направьте `proxy_pass` вашего Nginx на него. SSL обрабатывается хостом.
   - **Вариант Б: Чистый сервер (полное развертывание)**. 
     1. Установите `DOMAIN_NAME` и `ACME_EMAIL` в `.env`.
     2. В `docker-compose.yml` закомментируйте секцию `ports` сервиса `frontend`.
     3. Раскомментируйте сервис `caddy` внизу.
     4. Запустите `make up`. Caddy автоматически выпустит SSL-сертификаты.
7. Запустите:

```bash
make up
make migrate
```

Для продакшена используйте сложные учетные данные базы данных, ограничьте порты брандмауэром и терминируйте TLS перед сервисом фронтенда/nginx или замените его собственной конфигурацией HTTPS.

## Частые проблемы

`initData` пуст: приложение было открыто в обычном браузере. Откройте его внутри Telegram как Mini App.

Ошибка валидации хеша: `TELEGRAM_BOT_TOKEN` не совпадает с ботом, который открыл Mini App, `initData` были изменены или срок действия данных истек.

Ошибка CORS: добавьте источник вашего фронтенда в `BACKEND_CORS_ORIGINS`.

Mixed content (смешанный контент): ваш Mini App работает через HTTPS, но вызывает HTTP API. Настройте и фронтенд, и API через HTTPS.

Неверный токен бота: токены привязаны к конкретным ботам. Токен от другого бота не сможет проверить `initData` этого приложения.

## Тесты

Тесты бэкенда охватывают:

- эндпоинт health
- неверные `initData`
- юнит-тест валидной проверки HMAC Telegram
- отсутствие заголовка авторизации в `/api/users/me`

Запуск тестов в Docker:

```bash
make test
```

Запуск локально:

```bash
cd backend
python -m pip install -e ".[dev]"
pytest
```
