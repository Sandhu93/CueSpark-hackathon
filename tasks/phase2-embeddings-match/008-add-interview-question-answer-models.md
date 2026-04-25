# Task: Add Interview Question, Answer, Evaluation, Report, and Embedding Models

## Goal

Add the remaining core database models required for the interview engine, evaluation flow, reports, and vector storage.

## Scope

Implement only:

- `interview_questions` model.
- `candidate_answers` model.
- `answer_evaluations` model.
- `interview_reports` model.
- `embedding_chunks` model with pgvector field.
- Required Pydantic schemas.
- Model imports for database initialization.

## Out of Scope

Do not implement:

- Embedding generation.
- Question generation.
- TTS.
- Transcription.
- Evaluation logic.
- Frontend pages.

## Files Likely Involved

- `backend/app/models/`
- `backend/app/schemas/`
- `backend/app/models/__init__.py`
- `backend/app/core/db.py`

## API Contract

No new public endpoint is required in this task.

## Data Model Changes

Create models described in `docs/10-data-model-contract.md`:

- `interview_questions`
- `candidate_answers`
- `answer_evaluations`
- `interview_reports`
- `embedding_chunks`

## Acceptance Criteria

- [ ] All listed models exist.
- [ ] `embedding_chunks.embedding` uses the pgvector-compatible column type.
- [ ] Question category and source fields support documented values.
- [ ] Report hiring recommendation supports documented values.
- [ ] Models are imported during DB initialization.
- [ ] No AI calls are added.
- [ ] No API routes are added unless required for model verification.

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
- Use JSON/JSONB for structured flexible fields.
- Do not change existing table names without updating docs.
