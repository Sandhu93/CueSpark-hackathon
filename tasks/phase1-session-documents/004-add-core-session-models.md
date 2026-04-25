# Task: Add Core Session and Document Models

## Goal

Add the database models and Pydantic schemas needed to represent interview sessions and uploaded/pasted documents.

These models are the foundation for the later benchmark engine, but this task must not implement benchmark analysis itself.

## Scope

Implement only:

- `interview_sessions` model.
- `documents` model.
- Session/document enum values where appropriate.
- Fields needed later by match and benchmark phases, such as `role_key`, `match_score`, `benchmark_similarity_score`, `resume_competitiveness_score`, and `evidence_strength_score` if included in the current data contract.
- Pydantic schemas for create/read responses.
- Model imports required for database initialization.

## Out of Scope

Do not implement:

- Resume parsing.
- File upload endpoints.
- AI analysis.
- Embeddings.
- Benchmark profiles.
- Benchmark comparison.
- Question generation.
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

Follow `docs/10-data-model-contract.md` and `docs/03-database-design.md`.

Do not create benchmark tables in this task.

## Acceptance Criteria

- [ ] SQLAlchemy models exist for sessions and documents.
- [ ] Pydantic schemas exist for create/read use cases.
- [ ] Session status supports the documented lifecycle.
- [ ] Session model includes fields required later for match/benchmark summaries if defined in the data contract.
- [ ] Document parse status supports `pending`, `parsed`, `failed`, and `ocr_required`.
- [ ] Models are included in DB initialization/import flow.
- [ ] No API route is added in this task.
- [ ] No benchmark logic is added in this task.

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
- Keep this task as a foundation task. Benchmark implementation starts in `tasks/phase2-benchmark-engine/`.
