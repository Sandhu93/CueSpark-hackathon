# Task: Add Session API

## Goal

Add the first product API endpoints for creating and reading an interview session.

## Scope

Implement only:

- `POST /api/sessions`
- `GET /api/sessions/{session_id}`
- Request/response schemas for those endpoints.
- Minimal validation for empty job descriptions.
- Route registration in the FastAPI app.

## Out of Scope

Do not implement:

- Resume file upload.
- Session preparation jobs.
- AI match scoring.
- Question generation.
- Frontend pages.

## Files Likely Involved

- `backend/app/api/sessions.py`
- `backend/app/schemas/`
- `backend/app/models/`
- `backend/app/main.py` or router registration file
- `backend/tests/`

## API Contract

Follow `docs/09-api-contracts-detailed.md`.

### POST `/api/sessions`

Creates a session with status `draft`.

### GET `/api/sessions/{session_id}`

Returns session state.

## Data Model Changes

None beyond models created in the previous task.

## Acceptance Criteria

- [ ] `POST /api/sessions` creates an interview session.
- [ ] Empty or whitespace-only JD returns a validation error.
- [ ] Session starts with status `draft`.
- [ ] `GET /api/sessions/{session_id}` returns the session.
- [ ] Unknown session returns 404.
- [ ] No AI call happens in this task.
- [ ] No frontend change is required in this task.

## Verification

Run:

```bash
docker compose up --build
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"job_description":"Sample JD","resume_text":"Sample resume"}'
```

If tests exist:

```bash
pytest backend/tests
```

## Notes for Codex

- Keep route handlers thin.
- Put DB operations in a small service if the existing project style supports it.
