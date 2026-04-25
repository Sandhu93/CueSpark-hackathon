# AGENTS.md

Conventions for AI agents (Codex, Claude Code) working in this repo.

## Stack
- Backend: FastAPI + SQLAlchemy 2 (async) + Pydantic v2 + RQ on Redis + boto3 against MinIO.
- Frontend: Next.js 14 App Router + TypeScript + Tailwind.
- Orchestration: Docker Compose. Always assume services run inside compose.

## Code style
- Python: ruff-formatted, type hints on every public function, `from __future__ import annotations` at the top of any file with forward refs.
- TypeScript: strict mode is on. No `any` unless justified in a comment. Prefer named exports.
- No `print()` in backend code — use `loguru.logger`.
- No `console.log` in committed frontend code.

## Adding a new AI feature
1. Pydantic schemas in `backend/app/schemas/<feature>.py` — typed inputs and outputs.
2. Pure logic in `backend/app/services/<feature>.py` — no FastAPI, no DB. Easy to unit-test.
3. Background task in `backend/app/tasks/<feature>.py` — follow the `dummy.py` lifecycle.
4. Register the kind in `TASK_REGISTRY` in `backend/app/api/jobs.py`.
5. Frontend call via `api.createJob(...)` and `useJob(...)`.

## Don'ts
- Don't write business logic inside FastAPI route handlers — keep them thin.
- Don't share async SQLAlchemy sessions across worker tasks; use `tasks/_db.py:session_scope`.
- Don't put secrets in committed code; read from `app.core.config.settings`.
- Don't hand-write SQL when SQLAlchemy can do it.

## Tests
- `make test` runs pytest inside the api container.
- Add a test for any new endpoint and any new service function.
