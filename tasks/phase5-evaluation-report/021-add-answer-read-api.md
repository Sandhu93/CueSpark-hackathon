# Task: Add Answer Read API

## Goal

Expose candidate answer transcript, communication metrics, and evaluation result to the frontend.

## Scope

Implement only:

- `GET /api/answers/{answer_id}`.
- Response schema for answer details.
- Include evaluation if available.
- 404 handling for unknown answer.

## Out of Scope

Do not implement:

- New evaluation logic.
- Final report generation.
- Frontend UI.
- Reprocessing endpoints.

## Files Likely Involved

- `backend/app/api/interview.py`
- `backend/app/schemas/`
- `backend/app/models/`
- Router registration file
- `backend/tests/`

## API Contract

Follow `docs/09-api-contracts-detailed.md`.

## Data Model Changes

None.

## Acceptance Criteria

- [ ] Endpoint returns transcript when available.
- [ ] Endpoint returns communication metrics when available.
- [ ] Endpoint returns evaluation when available.
- [ ] Unknown answer returns 404.
- [ ] Endpoint does not trigger transcription or evaluation.
- [ ] No AI call happens in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual:

```bash
curl http://localhost:8000/api/answers/{answer_id}
```

## Notes for Codex

- This endpoint is read-only.
- Keep response stable for frontend integration.
