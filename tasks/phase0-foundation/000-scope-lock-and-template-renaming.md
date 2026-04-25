# Task 000 — Scope Lock and Template Renaming

## Goal

Convert the generic hackathon template identity into CueSpark Interview Coach without changing core architecture.

## Read First

- `AGENTS.md`
- `docs/00-project-overview.md`
- `docs/01-architecture.md`
- `docs/07-codex-development-rules.md`

## Requirements

1. Rename user-facing app labels from generic hackathon template to **CueSpark Interview Coach**.
2. Update FastAPI app title to `CueSpark Interview Coach API`.
3. Update README introduction to describe the new product.
4. Keep the existing Docker Compose services.
5. Keep existing `/health`, `/uploads`, and `/jobs` behavior working.
6. Do not add login, billing, dashboard, or real-time interview features.

## Files Likely Changed

- `README.md`
- `backend/app/main.py`
- `frontend/src/app/page.tsx`
- optional: `.env.example`

## Acceptance Criteria

- `docker compose up --build` still starts services.
- `GET /health` still returns status.
- Frontend no longer says generic hackathon template.
- No architecture changes were introduced.

## Out of Scope

- Database schema changes.
- AI integration.
- Interview flow.
- UI redesign beyond basic rename.
