# Task: Add Candidate vs Benchmark Analysis

## Goal

Compare the candidate resume against the retrieved benchmark profiles and produce a structured benchmark gap analysis.

## Scope

Implement only:

- `benchmark_analyzer.py` service.
- Pydantic schema for benchmark comparison output.
- Mock benchmark analysis when `AI_MOCK_MODE=true`.
- Real LLM analysis through centralized OpenAI client if available.
- Store output in `benchmark_comparisons`.

## Out of Scope

Do not implement:

- Question generation changes.
- Frontend UI.
- Final report changes.
- Live web scraping.
- Resume rewriting UI.

## Files Likely Involved

- `backend/app/services/benchmark_analyzer.py`
- `backend/app/services/prompts.py`
- `backend/app/models/`
- `backend/app/schemas/`
- `backend/app/tasks/`
- `backend/tests/`

## API Contract

No public endpoint is required unless wired through session preparation.

## Data Model Changes

Use existing `benchmark_comparisons` table.

## Output Requirements

Benchmark analysis should include:

- `benchmark_similarity_score`
- `resume_competitiveness_score`
- `evidence_strength_score`
- `missing_skills`
- `weak_skills`
- `missing_metrics`
- `weak_ownership_signals`
- `interview_risk_areas`
- `recommended_resume_fixes`
- `question_targets`

## Acceptance Criteria

- [ ] Analysis compares candidate resume against top benchmark profiles.
- [ ] Output is structured and typed.
- [ ] Mock mode works without OpenAI API key.
- [ ] Result is stored in `benchmark_comparisons`.
- [ ] Output includes interview risk areas.
- [ ] Output includes question targets for later question generation.
- [ ] No frontend changes are made.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification can use fixture JD/resume and seeded benchmark profiles.

## Notes for Codex

- Keep language strict and evidence-based.
- Do not claim the benchmark profiles are real hired candidates.
