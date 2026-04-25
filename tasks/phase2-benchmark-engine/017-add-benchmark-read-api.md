# Task: Add Benchmark Read API

## Goal

Expose the stored benchmark comparison for a prepared interview session so the frontend can render the benchmark gap dashboard.

This endpoint is required before building `/session/[sessionId]/benchmark` in the frontend.

## Scope

Implement only:

- `GET /api/sessions/{session_id}/benchmark`.
- Response schema for benchmark comparison details.
- Include retrieved benchmark profile summaries if available.
- Return stored benchmark comparison data.
- 404 handling for unknown session.
- Clear pending/not-found response when benchmark comparison is not ready yet.

## Out of Scope

Do not implement:

- Benchmark comparison generation.
- Benchmark profile seeding.
- Benchmark embedding/retrieval logic.
- Question generation.
- Frontend benchmark dashboard.
- Live scraping.
- Claims that benchmark profiles are verified hired/selected resumes.

## Files Likely Involved

- `backend/app/api/sessions.py`
- `backend/app/api/benchmark.py`
- `backend/app/schemas/benchmark.py`
- `backend/app/models/benchmark.py`
- Router registration file
- `backend/tests/`

## API Contract

Follow `docs/09-api-contracts-detailed.md`.

### GET `/api/sessions/{session_id}/benchmark`

Response:

```json
{
  "session_id": "uuid",
  "role_key": "backend_developer",
  "benchmark_similarity_score": 54,
  "resume_competitiveness_score": 48,
  "evidence_strength_score": 39,
  "benchmark_profiles": [
    {
      "id": "uuid",
      "profile_name": "Backend Benchmark 01",
      "role_title": "Backend Developer",
      "seniority_level": "mid",
      "quality_score": 88
    }
  ],
  "missing_skills": [],
  "weak_skills": [],
  "missing_metrics": [],
  "weak_ownership_signals": [],
  "interview_risk_areas": [],
  "recommended_resume_fixes": [],
  "question_targets": []
}
```

## Data Model Changes

None.

Use existing:

- `benchmark_comparisons`
- `benchmark_profiles`

## Acceptance Criteria

- [ ] `GET /api/sessions/{session_id}/benchmark` returns stored benchmark comparison data.
- [ ] Unknown session returns 404.
- [ ] Session without benchmark comparison returns a clear pending/not-found response.
- [ ] Response includes benchmark similarity, resume competitiveness, and evidence strength scores.
- [ ] Response includes missing skills, weak skills, missing metrics, weak ownership signals, interview risk areas, recommended resume fixes, and question targets.
- [ ] Response includes benchmark profile summaries when benchmark profile IDs are available.
- [ ] Endpoint does not generate benchmark analysis.
- [ ] Endpoint does not call OpenAI.
- [ ] Endpoint does not perform live scraping.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification:

```bash
curl http://localhost:8000/api/sessions/{session_id}/benchmark
```

## Notes for Codex

- Keep this endpoint read-only.
- Do not generate missing benchmark data inside this endpoint.
- The frontend benchmark dashboard depends on this endpoint.
- Use safe wording: benchmark profiles, role benchmark corpus, or curated top-candidate archetypes.
