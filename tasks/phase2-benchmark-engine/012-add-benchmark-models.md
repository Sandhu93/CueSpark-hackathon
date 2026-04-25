# Task: Add Benchmark Profile and Comparison Models

## Goal

Add database models required for the benchmark-driven novelty layer.

## Scope

Implement only:

- `benchmark_profiles` model.
- `benchmark_comparisons` model.
- Pydantic schemas for benchmark profile and comparison read/write use cases.
- Model imports for database initialization.
- Use existing `embedding_chunks` table for benchmark profile chunks.

## Out of Scope

Do not implement:

- Live web scraping.
- Benchmark fixture seeding.
- Embedding generation.
- Candidate-vs-benchmark analysis.
- Question generation.
- Frontend UI.

## Files Likely Involved

- `backend/app/models/`
- `backend/app/schemas/`
- `backend/app/models/__init__.py`
- `backend/app/core/db.py`

## API Contract

No public endpoint is required in this task.

## Data Model Changes

Create:

### `benchmark_profiles`

Recommended fields:

- `id`
- `role_key`
- `role_title`
- `seniority_level`
- `domain`
- `profile_name`
- `resume_text`
- `skills` JSON/JSONB
- `tools` JSON/JSONB
- `project_signals` JSON/JSONB
- `impact_signals` JSON/JSONB
- `ownership_signals` JSON/JSONB
- `source_type`: `curated | public | synthetic`
- `source_url`
- `is_curated`
- `quality_score`
- `created_at`

### `benchmark_comparisons`

Recommended fields:

- `id`
- `session_id`
- `role_key`
- `benchmark_profile_ids` JSON/JSONB
- `benchmark_similarity_score`
- `resume_competitiveness_score`
- `evidence_strength_score`
- `missing_skills` JSON/JSONB
- `weak_skills` JSON/JSONB
- `missing_metrics` JSON/JSONB
- `weak_ownership_signals` JSON/JSONB
- `interview_risk_areas` JSON/JSONB
- `recommended_resume_fixes` JSON/JSONB
- `question_targets` JSON/JSONB
- `created_at`

## Acceptance Criteria

- [ ] `benchmark_profiles` model exists.
- [ ] `benchmark_comparisons` model exists.
- [ ] Models use UUID primary keys.
- [ ] `benchmark_comparisons.session_id` links to an interview session.
- [ ] Flexible fields use JSON/JSONB.
- [ ] Models are imported by DB initialization.
- [ ] No scraping, AI calls, or frontend changes are added.

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

- This is the database foundation for novelty.
- Keep benchmark profiles curated/anonymized in the hackathon version.
