# Task: Add Core Session and Document Models

## Goal

Add the database models and Pydantic schemas needed to represent interview sessions and uploaded/pasted documents.

## Scope

Implement only:

- `interview_sessions` model.
- `documents` model.
- Session/document enum values where appropriate.
- Pydantic schemas for create/read responses.
- Model imports required for database initialization.

## Out of Scope

Do not implement:

- Resume parsing.
- File upload endpoints.
- AI analysis.
- Embeddings.
- Frontend pages.

## Files Likely Involved

- `backend/app/models/`
- `backend/app/schemas/`
- `backend/app/models/__init__.py`
- `backend/app/core/db.py`

## API Contract

No public endpoint is required in this task.

## Data Model Changes

Create only:

- `interview_sessions`
- `documents`

Follow `docs/10-data-model-contract.md`.

## Acceptance Criteria

- [ ] SQLAlchemy models exist for sessions and documents.
- [ ] Pydantic schemas exist for create/read use cases.
- [ ] Session status supports the documented lifecycle.
- [ ] Document parse status supports `pending`, `parsed`, `failed`, and `ocr_required`.
- [ ] Models are included in DB initialization/import flow.
- [ ] No API route is added in this task.

## Verification

Run:

```bash
docker compose up --build
```

If tests exist:

```bash
pytest backend/tests
```

## Notes for Codex

- Use UUID primary keys.
- Store large files in MinIO later; models should store object keys only.
