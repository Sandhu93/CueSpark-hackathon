# Hackathon Template — FastAPI + Next.js + Workers

A batteries-included starter for AI hackathons. One `docker compose up` and you have:

- **api** — FastAPI service (REST + WebSocket-ready)
- **worker** — Background worker (RQ / Redis Queue) for long-running AI jobs
- **web** — Next.js 14 (App Router) frontend
- **postgres** — Primary datastore
- **redis** — Cache + job queue + pub/sub
- **minio** — S3-compatible object storage for uploads (audio, video, PDFs, images)

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

| Service  | URL                       |
| -------- | ------------------------- |
| Web      | http://localhost:3000     |
| API      | http://localhost:8000     |
| API docs | http://localhost:8000/docs |
| MinIO    | http://localhost:9001 (console) |
| Postgres | localhost:5432            |
| Redis    | localhost:6379            |

Default MinIO credentials: `minioadmin` / `minioadmin` (change via `.env`).

## Project layout

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers
│   │   ├── core/         # config, logging, clients (redis, s3, db)
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas (request/response contracts)
│   │   ├── services/     # business logic
│   │   ├── tasks/        # background jobs called by the worker
│   │   └── workers/      # worker entrypoints
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js App Router pages
│   │   ├── components/
│   │   ├── hooks/
│   │   └── lib/          # api client, utils
│   ├── package.json
│   └── Dockerfile
├── infra/
│   └── minio-init.sh     # creates default bucket on startup
├── docker-compose.yml
└── .env.example
```

## Typical AI hackathon flow this template supports

1. User uploads a file from the Next.js frontend → API gets a presigned MinIO URL or uploads directly.
2. API enqueues a job to Redis (`tasks/`) and returns a `job_id` immediately.
3. Worker picks up the job, calls your AI pipeline (LLM, vision, STT, etc.), writes results to Postgres, caches hot results in Redis, stores artifacts in MinIO.
4. Frontend polls `/jobs/{id}` or subscribes via SSE/WebSocket for status.

## What to build first

- Drop your AI logic in `backend/app/services/` (one module per capability).
- Wire it into a job in `backend/app/tasks/`.
- Expose an endpoint in `backend/app/api/`.
- Call it from `frontend/src/lib/api.ts`.

## Ergonomics

- `make dev` — start everything with logs
- `make logs` — tail logs
- `make shell-api` — exec into the API container
- `make worker-restart` — restart just the worker after editing tasks
