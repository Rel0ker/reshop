.PHONY: help install install-dev test test-backend test-frontend lint lint-backend lint-frontend format format-backend format-frontend clean clean-backend clean-frontend docker-build docker-up docker-down migrate superuser run-backend run-frontend

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

install-dev: ## Установить зависимости для разработки
	python -m venv venv
	. venv/bin/activate && pip install -r requirements-dev.txt

test: test-backend test-frontend ## Запустить все тесты

test-backend: ## Запустить тесты backend
	. venv/bin/activate && python manage.py test

test-frontend: ## Запустить тесты frontend
	cd frontend-vue && npm test

lint: lint-backend lint-frontend ## Проверить код всех компонентов

lint-backend: ## Проверить код backend
	. venv/bin/activate && flake8 . && black --check . && isort --check-only .

lint-frontend: ## Проверить код frontend
	cd frontend-vue && npm run lint

format: format-backend format-frontend ## Отформатировать код всех компонентов

format-backend: ## Отформатировать код backend
	. venv/bin/activate && black . && isort .

format-frontend: ## Отформатировать код frontend
	cd frontend-vue && npm run format

clean: clean-backend clean-frontend ## Очистить все временные файлы

clean-backend: ## Очистить временные файлы backend
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -delete
	rm -rf .coverage htmlcov

clean-frontend: ## Очистить временные файлы frontend
	cd frontend-vue && rm -rf node_modules dist .nuxt .next

docker-build: ## Собрать Docker образы
	docker-compose build

docker-up: ## Запустить Docker контейнеры
	docker-compose up -d

docker-down: ## Остановить Docker контейнеры
	docker-compose down

migrate: ## Применить миграции
	. venv/bin/activate && python manage.py migrate

superuser: ## Создать суперпользователя
	. venv/bin/activate && python manage.py createsuperuser

run-backend: ## Запустить backend сервер
	. venv/bin/activate && python manage.py runserver

run-frontend: ## Запустить frontend сервер
	cd frontend-vue && npm run dev

setup: install migrate ## Полная настройка проекта
	@echo "Проект настроен! Запустите 'make run-backend' и 'make run-frontend' в разных терминалах"

dev: run-backend run-frontend ## Запустить оба сервера (в фоне)
	@echo "Запуск в фоне..."
	@make run-backend &
	@make run-frontend &
	@echo "Серверы запущены в фоне. Используйте 'make stop-dev' для остановки"

stop-dev: ## Остановить все фоновые процессы
	@echo "Остановка серверов..."
	@pkill -f "python manage.py runserver"
	@pkill -f "npm run dev"
	@echo "Серверы остановлены"

