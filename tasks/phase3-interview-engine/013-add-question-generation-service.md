# Task: Add Question Generation Service

## Goal

Generate and store a 10-question mixed interview plan for a prepared session.

## Scope

Implement only:

- `question_generator.py` service.
- Prompt registry entry for question generation.
- Pydantic schema for generated questions.
- Mock question generation when `AI_MOCK_MODE=true`.
- Store 10 base questions in `interview_questions`.

## Out of Scope

Do not implement:

- Adaptive follow-up generation.
- TTS.
- Candidate answer upload.
- Evaluation.
- Final report.
- Frontend interview UI.

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

## Acceptance Criteria

- [ ] Service generates exactly 10 base questions.
- [ ] Questions include category, difficulty, expected signal, and reason/provenance where available.
- [ ] Generated categories cover the documented mixed interview categories where appropriate.
- [ ] Mock mode works without OpenAI API key.
- [ ] Real mode uses centralized OpenAI client and prompt registry if implemented.
- [ ] Questions are stored with `source=base_plan`.
- [ ] No TTS is generated in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification can use fixture JD/resume and inspect stored questions.

## Notes for Codex

- For non-software roles, `technical` means role-specific competency.
- Do not make this a generic chatbot.
