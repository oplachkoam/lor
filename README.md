# Трекер персонажей Властелина колец (LOR)

> **Автор:** Оплачко Александр Матвеевич
>
> **Задача:** №6

> **[Ссылка на видео](https://drive.google.com/file/d/1WndLwmtpLxWoitCtjyRucFBQm2S6AzU7/view?usp=sharing)**
>
> **[Сайт](http://195.133.25.97)**

Современное веб-приложение для управления информацией
о персонажах и локациях вселенной "Властелин Колец".
Построено на FastAPI (Python) с фронтендом на Svelte
и использует слоистую архитектуру.

## Особенности

### Архитектура

- **Слоистая архитектура** - четкое разделение на слои: routes, storage, dto
- **Асинхронность** - полностью асинхронный код с использованием asyncio и asyncpg
- **Type Safety** - строгая типизация и валидация с использованием Pydantic

### Технологический стек

#### Backend

- **Python 3.13+** - основной язык разработки
- **FastAPI** - асинхронный веб-фреймворк
- **asyncpg** - асинхронный драйвер PostgreSQL
- **Uvicorn** - ASGI сервер
- **Pydantic** - валидация данных и сериализация

#### Frontend

- **Svelte** - современный SPA фреймворк
- **Vite** - сборщик и dev-сервер
- **Nginx** - веб-сервер для продакшена

#### Database & Infrastructure

- **PostgreSQL** - реляционная база данных
- **Docker & Docker Compose** - контейнеризация
- **uv** - современный менеджер пакетов Python

### DevOps

- **Docker контейнеризация** - готовые к продакшену образы
- **Health checks** - мониторинг состояния сервисов
- **Миграции БД** - автоматическое управление схемой
- **Automated testing** - тесты с pytest
- **CORS поддержка** - настроенный CORS middleware

## Структура проекта

```
LOR
├── src/                   # Backend исходный код
│   ├── main.py            # Точка входа приложения
│   ├── database/          # Слой работы с БД
│   │   └── postgres.py    # Подключение к PostgreSQL
│   ├── dto/               # Data Transfer Objects
│   │   ├── characters.py  # DTO для персонажей
│   │   ├── locations.py   # DTO для локаций
│   │   └── errors.py      # Модели ошибок
│   ├── routes/            # HTTP роуты (API endpoints)
│   │   ├── characters.py  # Роуты для персонажей
│   │   └── locations.py   # Роуты для локаций
│   └── storage/           # Слой хранения данных
│       ├── characters.py  # Хранилище персонажей
│       └── locations.py   # Хранилище локаций
├── frontend/              # Frontend приложение
│   ├── src/              
│   │   ├── App.svelte    # Главный компонент
│   │   ├── lib/          # Компоненты библиотеки
│   │   │   ├── Characters.svelte
│   │   │   ├── Locations.svelte
│   │   │   └── ConfirmModal.svelte
│   │   └── config.js     # Конфигурация
│   ├── dist/             # Собранное приложение
│   └── nginx.conf        # Конфигурация Nginx
├── migrations/           # SQL миграции
│   ├── 001_added_uuid.sql
│   ├── 002_added_characters.sql
│   ├── 003_added_locations.sql
│   ├── 004_added_data.sql
│   └── migrator.py       # Скрипт миграций
├── test/                 # Тесты
│   ├── conftest.py       # Конфигурация pytest
│   ├── test_characters.py
│   └── test_locations.py
├── docker-compose.yml       # Основной Docker Compose
├── docker-compose.test.yml  # Docker Compose для тестов
├── Dockerfile               # Backend Dockerfile
├── Makefile                 # Команды разработки
└── pyproject.toml           # Python зависимости
```

## Установка и запуск

### Предварительные требования

- **Docker** и **Docker Compose**
- **uv** (для локальной разработки)
- **Make** (для локальной разработки)
- **Python 3.13+** (для локальной разработки)
- **Node.js 18+** (для разработки фронтенда)

### Быстрый старт

1. **Клонируйте репозиторий**

```bash
git clone https://github.com/oplachkoam/lor.git
cd lor
```

2. **Создайте файл окружения**

```bash
cp .env.example .env
# Выставите требуемые параметры
```

3. **Запустите проект**

```bash
make start
# или
docker compose up --build
```

После запуска:

- **Backend API** будет доступен на: http://localhost:8000
- **API документация** (Swagger): http://localhost:8000/docs
- **Frontend** будет доступен на: http://localhost
- **PostgreSQL** будет доступен на: localhost:5432

### Доступные команды

```bash
make start       # Запуск всех сервисов (с пересборкой)
make start-d     # Запуск в фоновом режиме
make stop        # Остановка сервисов
make logs        # Просмотр логов backend сервера
make migrate     # Выполнение миграций БД
make test        # Запуск интеграционных тестов
make lint        # Проверка кода линтером (flake8)
make format      # Форматирование кода (autopep8 + isort)
make delete      # Удаление контейнеров
make delete-data # Удаление контейнеров и volumes (БД)
```

## Дальнейшие улучшения

### TODO: Возможные расширения функциональности

- [ ] **Аутентификация** - добавление JWT auth для безопасности API
- [ ] **Пагинация** - поддержка limit/offset для больших списков
- [ ] **Фильтрация** - поиск персонажей по имени, локации
- [ ] **Связи между сущностями** - отображение всех персонажей локации
- [ ] **Валидация координат** - проверка допустимых значений X, Y
- [ ] **Загрузка изображений** - поддержка аватаров персонажей
- [ ] **WebSocket** - real-time обновления при изменении данных
- [ ] **Логирование** - structured logging с использованием loguru
- [ ] **CI/CD** - автоматическое тестирование и деплой

## Лицензия

Проект создан в рамках отбора на кафедру 1С МФТИ

## Контакты

**Telegram:** @op1alex
