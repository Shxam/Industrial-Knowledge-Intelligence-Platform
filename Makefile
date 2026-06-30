# Makefile for IKIP Development

.PHONY: help setup start stop restart logs clean test lint format

help:
	@echo "IKIP (Pragya) - Development Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup      - Initial project setup"
	@echo "  make install    - Install dependencies"
	@echo ""
	@echo "Services:"
	@echo "  make start      - Start all services"
	@echo "  make stop       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - View service logs"
	@echo "  make ps         - Show service status"
	@echo ""
	@echo "Development:"
	@echo "  make dev-backend  - Run backend in dev mode"
	@echo "  make dev-frontend - Run frontend in dev mode"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo ""
	@echo "Database:"
	@echo "  make db-migrate   - Run database migrations"
	@echo "  make db-reset     - Reset database"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Clean temporary files"
	@echo "  make clean-all    - Clean everything (including data)"

setup:
	@echo "Running setup script..."
	python setup.py

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

start:
	@echo "Starting Docker services..."
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	sleep 10
	docker-compose ps

stop:
	@echo "Stopping Docker services..."
	docker-compose down

restart: stop start

logs:
	docker-compose logs -f

ps:
	docker-compose ps

dev-backend:
	@echo "Starting backend in development mode..."
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	@echo "Starting frontend in development mode..."
	cd frontend && npm start

test:
	@echo "Running backend tests..."
	cd backend && pytest
	@echo "Running frontend tests..."
	cd frontend && npm test

lint:
	@echo "Linting backend..."
	cd backend && flake8 app/
	cd backend && mypy app/
	@echo "Linting frontend..."
	cd frontend && npm run lint

format:
	@echo "Formatting backend code..."
	cd backend && black app/
	@echo "Formatting frontend code..."
	cd frontend && npm run format

db-migrate:
	@echo "Running database migrations..."
	cd backend && alembic upgrade head

db-reset:
	@echo "Resetting database..."
	docker-compose down -v
	docker-compose up -d postgres
	sleep 5
	make db-migrate

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf backend/logs/*.log 2>/dev/null || true

clean-all: clean
	@echo "Cleaning all data and volumes..."
	docker-compose down -v
	rm -rf data/faiss_index/*
	rm -rf data/uploads/*
	rm -rf data/processed/*
	rm -rf backend/venv
	rm -rf frontend/node_modules
	rm -rf frontend/build

.DEFAULT_GOAL := help
