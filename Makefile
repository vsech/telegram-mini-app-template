COMPOSE := docker compose

.PHONY: up down logs backend-shell frontend-shell migrate makemigration test lint format

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

backend-shell:
	$(COMPOSE) exec backend sh

frontend-shell:
	$(COMPOSE) exec frontend sh

migrate:
	$(COMPOSE) exec backend alembic upgrade head

makemigration:
	$(COMPOSE) exec backend alembic revision --autogenerate -m "$(m)"

test:
	$(COMPOSE) exec backend pytest

lint:
	$(COMPOSE) exec backend ruff check .
	docker build --target build -t telegram-mini-app-template-frontend-build ./frontend
	docker run --rm telegram-mini-app-template-frontend-build npm run lint

format:
	$(COMPOSE) exec backend ruff format .
	docker run --rm -v "$(PWD)/frontend:/app" -w /app node:22-alpine sh -c "npm install && npm run format"
