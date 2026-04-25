# Architecture

## Request shape

```
            ┌──────────┐  PUT (presigned)   ┌──────────┐
            │   web    │ ─────────────────▶ │  minio   │
            └────┬─────┘                    └──────────┘
                 │ POST /jobs                     ▲
                 ▼                                │ get/put
            ┌──────────┐  enqueue          ┌──────┴─────┐
            │   api    │ ─────────────────▶│   redis    │
            └────┬─────┘                    └──────┬─────┘
                 │ writes job row                  │ pulls jobs
                 ▼                                 ▼
            ┌──────────┐                     ┌──────────┐
            │ postgres │◀────────────────────│  worker  │
            └──────────┘   updates status    └──────────┘
```

## Why these specific pieces

- **FastAPI** for the API: typed bodies via Pydantic, async, OpenAPI for free at `/docs`.
- **RQ on Redis** for jobs: zero infra to learn vs Celery; tasks are plain Python functions.
- **MinIO** for storage: S3 API locally, so production-day swap to AWS/Cloudflare R2 is one env var.
- **Postgres** for state: durable record of every job and its result.
- **Next.js App Router** for web: server components when you want them, client components for interactive bits like polling.

## Adding a new AI capability

1. Define typed inputs/outputs in `backend/app/schemas/<thing>.py`.
2. Write the pure logic in `backend/app/services/<thing>.py` — no FastAPI, no DB, just functions.
3. Wrap it in a task in `backend/app/tasks/<thing>.py` following the lifecycle pattern in `dummy.py`.
4. Register the task kind in `TASK_REGISTRY` in `backend/app/api/jobs.py`.
5. Call from the frontend with `api.createJob("<kind>", { … })` and poll with `useJob`.

This separation matters: keeping `services/` free of FastAPI and DB means you can unit-test the AI logic without spinning up the whole stack.

## What to swap for production

- Switch MinIO to S3 / R2 by changing `minio_endpoint` and credentials.
- Move secrets out of `.env` into a real secret manager.
- Add Alembic migrations instead of `Base.metadata.create_all`.
- Put a reverse proxy (Caddy / nginx) in front and terminate TLS.
- Replace `--reload` with a proper uvicorn worker count, and run web with `next start`.
