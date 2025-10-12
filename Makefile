.PHONY: lint format logs test start start-d stop delete migrate delete-data

lint:
	@echo "==> Линтер"
	uv run flake8 src

format:
	@echo "==> Форматирование"
	uv run autopep8 --in-place --recursive src && uv run isort src

logs:
	@echo "==> Логи"
	docker logs lor-server

test:
	@echo "==> Тесты"
	docker-compose -f docker-compose.test.yml down -v
	docker-compose -f docker-compose.test.yml up -d
	sleep 10
	uv run pytest test
	docker compose -f docker-compose.test.yml down -v

start:
	@echo "==> Запуск"
	docker compose up --build

start-d:
	@echo "==> Запуск в фоне"
	docker compose up --build -d

stop:
	@echo "==> Остановка"
	docker compose stop

delete:
	@echo "==> Удаление контейнеров"
	docker compose down --remove-orphans

migrate:
	@echo "==> Миграции"
	docker compose up --build --abort-on-container-exit migrator

delete-data:
	@echo "==> Удаление данных"
	docker compose down -v
