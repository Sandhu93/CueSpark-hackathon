# Task: Add Interview Question, Answer, Evaluation, Report, and Embedding Models

## Goal

Add the remaining core database models required for the interview engine, evaluation flow, reports, and vector storage.

These models should be benchmark-ready, but this task must not implement benchmark profiles or benchmark comparison tables.

## Scope

Implement only:

- `interview_questions` model.
- `candidate_answers` model.
- `answer_evaluations` model.
- `interview_reports` model.
- `embedding_chunks` model with pgvector field.
- Benchmark-ready fields already defined in `docs/10-data-model-contract.md`, such as `benchmark_gap_refs`, `why_this_was_asked`, `benchmark_gap_coverage_score`, and benchmark-aware report score fields if included in the contract.
- Required Pydantic schemas.
- Model imports for database initialization.

## Out of Scope

Do not implement:

- Benchmark profiles.
- Benchmark comparison tables.
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

Do not create `benchmark_profiles` or `benchmark_comparisons` here. Those belong to `tasks/phase2-benchmark-engine/012-add-benchmark-models.md`.

## Acceptance Criteria

- [ ] All listed models exist.
- [ ] `embedding_chunks.embedding` uses the pgvector-compatible column type.
- [ ] `embedding_chunks` supports `benchmark_profile` as a valid future chunk type if defined in the data contract.
- [ ] Question category and source fields support documented benchmark-aware values.
- [ ] Report model supports benchmark-aware report fields defined in the data contract.
- [ ] Report hiring recommendation supports documented values.
- [ ] Models are imported during DB initialization.
- [ ] No AI calls are added.
- [ ] No benchmark profiles/comparisons are added.
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
- Follow `docs/10-data-model-contract.md` exactly.
