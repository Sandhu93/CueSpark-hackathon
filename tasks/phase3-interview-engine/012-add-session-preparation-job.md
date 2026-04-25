# Task: Add Session Preparation Job

## Goal

Create the background job that prepares a session by parsing available text, chunking, embedding, and generating match analysis.

## Scope

Implement only:

- `POST /api/sessions/{session_id}/prepare` if not already implemented.
- `prepare_session` worker task.
- Session status transitions: `draft` → `preparing` → `ready` or `failed`.
- Use existing parser/chunking/embedding/match services.
- Return a `job_id` to the frontend.

## Out of Scope

Do not implement:

- Question generation unless explicitly done in a later task.
- TTS.
- Candidate recording.
- Report generation.
- Frontend interview UI.

## Files Likely Involved

- `backend/app/api/sessions.py`
- `backend/app/api/jobs.py`
- `backend/app/tasks/prepare_session.py`
- `backend/app/tasks/_db.py`
- `backend/app/services/`
- `backend/app/models/`

## API Contract

Follow `docs/09-api-contracts-detailed.md`.

### POST `/api/sessions/{session_id}/prepare`

Response:

```json
{
  "job_id": "string",
  "status": "queued"
}
```

## Data Model Changes

None unless required by previous missing models.

## Acceptance Criteria

- [ ] Endpoint enqueues a preparation job.
- [ ] Worker task updates session status to `preparing`.
- [ ] Worker task chunks and embeds JD/resume text.
- [ ] Worker task generates match analysis.
- [ ] Worker task updates session status to `ready` on success.
- [ ] Worker task updates session status to `failed` on failure.
- [ ] Job status can be checked using the existing job system.
- [ ] No questions are generated in this task.

## Verification

Run:

```bash
docker compose up --build
```

Then:

```bash
curl -X POST http://localhost:8000/api/sessions/{session_id}/prepare
```

Check worker logs:

```bash
docker compose logs -f worker
```

## Notes for Codex

- Use `tasks/_db.py:session_scope` if present.
- Do not duplicate DB session handling patterns.
