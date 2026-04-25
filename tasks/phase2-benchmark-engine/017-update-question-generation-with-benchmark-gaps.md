# Task: Update Question Generation with Benchmark Gaps

## Goal

Make interview question generation benchmark-driven instead of only JD/resume-driven.

## Scope

Implement only:

- Update question generation input to include benchmark comparison output.
- Generate questions from benchmark gap targets where available.
- Store benchmark gap reference/provenance in question metadata where supported.
- Keep the total interview plan at 10 base questions.

## Out of Scope

Do not implement:

- Adaptive follow-ups.
- Frontend changes.
- TTS changes.
- Final report changes.
- Live web scraping.

## Files Likely Involved

- `backend/app/services/question_generator.py`
- `backend/app/services/prompts.py`
- `backend/app/models/`
- `backend/app/schemas/`
- `backend/app/tasks/`

## API Contract

No new public endpoint is required.

## Data Model Changes

Use existing `interview_questions` fields and metadata if available.

If metadata is not available, add a minimal JSON/JSONB field only if necessary:

```txt
benchmark_gap_refs
```

## Question Generation Rule

Questions should be generated from:

```txt
JD requirements + candidate resume + match analysis + benchmark comparison gaps
```

Priority should be:

1. High-risk benchmark gaps
2. Missing metrics/evidence
3. Weak ownership signals
4. JD skill validation
5. Behavioral/HR validation

## Acceptance Criteria

- [ ] Question generation uses benchmark comparison when available.
- [ ] At least 4 of 10 questions are directly tied to benchmark gaps when benchmark data exists.
- [ ] Questions include strict interviewer framing.
- [ ] Question provenance mentions whether it came from JD, resume, or benchmark gap.
- [ ] Mock mode still works without OpenAI API key.
- [ ] No frontend changes are made.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification:

1. Seed benchmark profiles.
2. Prepare a session.
3. Generate questions.
4. Confirm questions target missing metrics, evidence, ownership, and skill gaps.

## Notes for Codex

- This is the main novelty integration point.
- Do not generate generic questions if benchmark gaps exist.
