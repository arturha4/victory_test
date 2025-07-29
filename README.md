# VictoryTest

Тестовое VictoryGroup

## Технологии
* AsyncPG
* aiogram
* SQLAlchemy
* Docker


## Требования

- Установленный Docker (https://docs.docker.com/get-docker/)
- Установленный Docker Compose (https://docs.docker.com/compose/install/)
- Python 3.11
## Быстрый старт

1. Клонируйте репозиторий:
   git clone https://github.com/arturha4/victory_test.git

2. Скопируйте и настройте файл переменных окружения:
   - .env
   - Отредактируйте .env при необходимости (например, вставьте токен бота, настройки БД)

3. Запустите сервис с бд с помощью Docker Compose:
   - docker-compose -f docker-compose-pg.yaml up -d

4. В другом терминале примените миграции базы данных:
-  Перейдите в корень проекта 
-     alembic upgrade head
-     python bot.py

5. После этого бот и сервисы готовы к работе.
## Структура проекта
- app/ - логика бота
- database/ - работа с асинхронной бд
- migration/ — миграции Alembic для базы данных
- config.py - класс для импорта переменных из .env
- docker-compose-pg.yml — конфигурация запуска postgres
- .env — пример файла с переменными окружения
- requirements.txt — зависимости Python-проекта

## Переменные окружения (.env)
POSTGRES_USER=postgres\
POSTGRES_PASSWORD=postgres\
POSTGRES_DB=postgres\
POSTGRES_HOST=db\
POSTGRES_PORT=5432\
TELEGRAM_BOT_TOKEN = токен бота из BotFather\
TELEGRAM_BOT_ADMIN_ID=Telegram id админа

## Как работают сервисы

- PostgreSQL запускается как отдельный контейнер.
- Приложение (бот) зависит от базы данных и запускается после её готовности.
- Перед стартом бота запускаете процесс миграций через Alembic.

## Полезные команды

- Запуск всех сервисов:
  docker compose up --build

- Остановка сервисов:
  docker compose down
