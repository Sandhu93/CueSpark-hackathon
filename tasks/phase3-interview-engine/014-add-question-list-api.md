# Task: Add Question List API

## Goal

Expose stored interview questions for a prepared session.

## Scope

Implement only:

- `GET /api/sessions/{session_id}/questions`.
- Response schema for question list.
- Basic ordering by question number.
- 404 handling for unknown session.

## Out of Scope

Do not implement:

- TTS generation.
- Answer upload.
- Evaluation.
- Frontend interview UI.
- Adaptive follow-ups.

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

- [ ] Endpoint returns questions for a session.
- [ ] Questions are ordered by `question_number`.
- [ ] Response includes `id`, `question_number`, `category`, `difficulty`, `question_text`, `expected_signal`, and `tts_audio_url` if available.
- [ ] Unknown session returns 404.
- [ ] Session with no questions returns an empty list or appropriate state response consistently.
- [ ] No AI call happens in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual:

```bash
curl http://localhost:8000/api/sessions/{session_id}/questions
```

## Notes for Codex

- Keep this endpoint read-only.
- Do not generate questions inside this endpoint.
