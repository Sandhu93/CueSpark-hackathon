# Task 011 — Session and Document Ingestion

## Goal

Implement session creation and document ingestion for pasted JD, pasted resume, and uploaded resume object references.

## Read First

- `docs/00-project-overview.md`
- `docs/02-backend-design.md`
- `docs/06-api-contracts.md`

## Requirements

1. Add `backend/app/api/sessions.py`.
2. Implement `POST /sessions`.
3. Implement `GET /sessions/{session_id}`.
4. Implement `POST /sessions/{session_id}/prepare` that enqueues `prepare_session` job.
5. Create initial `Document` rows for:
   - job description paste
   - resume paste, if provided
   - resume upload reference, if provided
6. Register `prepare_session` task kind in `TASK_REGISTRY`.
7. Add a placeholder `backend/app/tasks/prepare_session.py` that updates status but does not yet call AI.

## Request Shape

```json
{
  "job_description_text": "string",
  "resume_text": "string optional",
  "resume_object_key": "string optional",
  "resume_filename": "string optional"
}
```

## Behavior

- Session starts with `created` status.
- Calling prepare changes it to `preparing`, enqueues job, and eventually marks it `ready` in placeholder mode.
- Do not require login.

## Files Likely Changed

- `backend/app/api/sessions.py`
- `backend/app/main.py`
- `backend/app/api/jobs.py`
- `backend/app/tasks/prepare_session.py`
- `backend/app/schemas/session.py`
- tests as practical

## Acceptance Criteria

- `POST /sessions` creates a session.
- `GET /sessions/{id}` returns it.
- `POST /sessions/{id}/prepare` returns a job id.
- Existing upload endpoints still work.

## Out of Scope

- Actual parsing.
- Actual embeddings.
- Actual question generation.
- Frontend implementation.
