.PHONY: dev up down logs ps build rebuild \
        shell-api shell-worker shell-web \
        worker-restart api-restart \
        psql redis-cli minio-console \
        test lint format

# ---------- lifecycle ----------
dev: up logs

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

ps:
	docker compose ps

build:
	docker compose build

rebuild:
	docker compose build --no-cache

# ---------- shells ----------
shell-api:
	docker compose exec api bash

shell-worker:
	docker compose exec worker bash

shell-web:
	docker compose exec web sh

# ---------- targeted restarts ----------
worker-restart:
	docker compose restart worker

api-restart:
	docker compose restart api

# ---------- data layer ----------
psql:
	docker compose exec postgres psql -U app -d app

redis-cli:
	docker compose exec redis redis-cli

minio-console:
	@echo "open http://localhost:9001  (minioadmin / minioadmin)"

# ---------- quality ----------
test:
	docker compose exec api pytest -q

lint:
	docker compose exec api ruff check app

format:
	docker compose exec api ruff format app
