# Task 010 — Core Models and Schemas

## Goal

Create the core database models and Pydantic schemas for sessions, documents, questions, answers, evaluations, reports, and embeddings.

## Read First

- `docs/02-backend-design.md`
- `docs/03-database-design.md`
- `docs/06-api-contracts.md`

## Requirements

Create SQLAlchemy models for:

1. `InterviewSession`
2. `Document`
3. `InterviewQuestion`
4. `CandidateAnswer`
5. `AnswerEvaluation`
6. `InterviewReport`
7. `EmbeddingChunk`

Create Pydantic schemas for request/response contracts.

## Important Notes

- Use simple string/UUID primary keys consistent with the existing `Job` model.
- Use JSON/JSONB for flexible metadata.
- Use pgvector-compatible column for embeddings.
- If pgvector SQLAlchemy integration is inconvenient initially, create the model with a clear TODO and raw column type only if it works safely. Do not break app startup.
- Ensure `init_db()` imports/registers the new models.

## Files Likely Changed

- `backend/app/models/session.py`
- `backend/app/models/document.py`
- `backend/app/models/question.py`
- `backend/app/models/answer.py`
- `backend/app/models/evaluation.py`
- `backend/app/models/report.py`
- `backend/app/models/embedding.py`
- `backend/app/models/__init__.py`
- `backend/app/schemas/session.py`
- `backend/app/schemas/document.py`
- `backend/app/schemas/question.py`
- `backend/app/schemas/answer.py`
- `backend/app/schemas/evaluation.py`
- `backend/app/schemas/report.py`
- `backend/app/schemas/embedding.py`
- `backend/app/core/db.py`

## Acceptance Criteria

- App starts and creates new tables.
- Existing `jobs` table still works.
- New schemas import successfully.
- No endpoint implementation required yet.

## Out of Scope

- AI logic.
- Frontend pages.
- File parsing.
