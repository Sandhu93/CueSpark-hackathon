# Task: Add Benchmark-Driven Question Generation Service

## Goal

Generate and store a 10-question mixed interview plan for a prepared session using JD, resume, match analysis, and benchmark gap analysis.

## Scope

Implement only:

- `question_generator.py` service.
- Prompt registry entry for benchmark-driven question generation.
- Pydantic schema for generated questions.
- Mock question generation when `AI_MOCK_MODE=true`.
- Store 10 base questions in `interview_questions`.
- Include question provenance and `why_this_was_asked`.
- Include benchmark gap references where available.

## Out of Scope

Do not implement:

- Adaptive follow-up generation.
- TTS.
- Candidate answer upload.
- Evaluation.
- Final report.
- Frontend interview UI.
- Benchmark comparison logic itself.

## Files Likely Involved

- `backend/app/services/question_generator.py`
- `backend/app/services/prompts.py`
- `backend/app/schemas/`
- `backend/app/models/`
- `backend/app/tasks/`

## API Contract

No new public endpoint is required unless the task is wired into session preparation.

## Data Model Changes

Use existing `interview_questions` table.

## Question Generation Inputs

Use available context:

- job description
- resume text or resume summary
- match analysis
- benchmark comparison
- benchmark question targets
- interview risk areas

## Acceptance Criteria

- [ ] Service generates exactly 10 base questions.
- [ ] Questions include category, difficulty, expected signal, source, provenance, and reason/`why_this_was_asked` where available.
- [ ] At least 4 of 10 questions are directly tied to benchmark gaps when benchmark data exists.
- [ ] Questions include benchmark gap references where available.
- [ ] Generated categories cover the documented mixed interview categories where appropriate.
- [ ] Mock mode works without OpenAI API key.
- [ ] Real mode uses centralized OpenAI client and prompt registry if implemented.
- [ ] Questions tied to benchmark gaps are stored with `source=benchmark_gap` where supported.
- [ ] No TTS is generated in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification can use fixture JD/resume and seeded benchmark profiles, then inspect stored questions.

## Notes for Codex

- For non-software roles, `technical` means role-specific competency.
- Do not make this a generic chatbot.
- Do not generate generic questions when benchmark gaps are available.
