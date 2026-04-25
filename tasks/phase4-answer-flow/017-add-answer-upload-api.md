# Task: Add Candidate Answer Upload API

## Goal

Allow the frontend to upload a candidate's recorded answer audio for a specific interview question.

## Scope

Implement only:

- `POST /api/questions/{question_id}/answers` endpoint.
- Store uploaded audio in MinIO.
- Create `candidate_answers` row.
- Enqueue transcription/evaluation job if task registry supports it, or return answer ID for later processing.

## Out of Scope

Do not implement:

- Transcription logic.
- Answer evaluation logic.
- Final report.
- Frontend polish.
- Video upload.

## Files Likely Involved

- `backend/app/api/interview.py`
- `backend/app/api/audio.py`
- `backend/app/services/storage.py`
- `backend/app/models/`
- `backend/app/schemas/`
- `backend/app/api/jobs.py`

## API Contract

Follow `docs/09-api-contracts-detailed.md`.

## Data Model Changes

Use existing `candidate_answers` table.

## Acceptance Criteria

- [ ] Endpoint accepts audio file upload.
- [ ] Endpoint validates allowed audio formats.
- [ ] Audio is stored in MinIO.
- [ ] Candidate answer row is created.
- [ ] Response includes `answer_id`.
- [ ] Unknown question returns 404.
- [ ] No transcription is implemented in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual upload through API docs is acceptable.

## Notes for Codex

- Do not store audio binary in Postgres.
- Do not expose permanent MinIO credentials.
