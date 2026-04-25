# Task: Verify Local Docker Stack

## Goal

Confirm that the existing local development stack boots correctly before adding CueSpark-specific features.

## Scope

Implement only:

- Inspect the current Docker Compose setup.
- Verify expected services: API, web, worker, Postgres, Redis, MinIO.
- Add or update minimal documentation only if commands are missing or inaccurate.
- Identify any broken service names, ports, or environment variable mismatches.

## Out of Scope

Do not implement:

- Interview session models.
- pgvector changes.
- AI/OpenAI integration.
- Frontend redesign.
- New services.

## Files Likely Involved

- `docker-compose.yml`
- `.env.example`
- `README.md`
- `Makefile`
- `backend/app/core/config.py`
- `frontend/src/lib/api.ts`

## API Contract

No new API endpoint is required in this task.

## Data Model Changes

None.

## Acceptance Criteria

- [ ] `docker compose up --build` starts the local stack.
- [ ] API is reachable at `http://localhost:8000`.
- [ ] API docs are reachable at `http://localhost:8000/docs`.
- [ ] Web app is reachable at `http://localhost:3000`.
- [ ] Postgres, Redis, and MinIO containers start without crash loops.
- [ ] Worker container starts and connects to Redis.
- [ ] `.env.example` contains the variables needed to boot the stack.
- [ ] No CueSpark product features are added in this task.

## Verification

Run:

```bash
docker compose up --build
docker compose ps
docker compose logs api --tail=100
docker compose logs worker --tail=100
```

Optional:

```bash
curl http://localhost:8000/docs
```

## Notes for Codex

- This is a foundation check only.
- Prefer documenting issues over making broad architectural changes.
- Do not refactor unrelated files.
