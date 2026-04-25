# Task: Add Answer Evaluation Service

## Goal

Evaluate each candidate answer using the question, expected signal, JD/resume context, transcript, and communication metrics.

## Scope

Implement only:

- `answer_evaluator.py` service.
- Prompt registry entry for answer evaluation.
- Pydantic output schema for evaluation.
- Mock evaluation when `AI_MOCK_MODE=true`.
- Worker task for evaluating an answer.
- Store results in `answer_evaluations`.

## Out of Scope

Do not implement:

- Final report generation.
- Adaptive follow-ups.
- Frontend report UI.
- Video analysis.

## Files Likely Involved

- `backend/app/services/answer_evaluator.py`
- `backend/app/services/prompts.py`
- `backend/app/tasks/evaluate_answer.py`
- `backend/app/models/`
- `backend/app/schemas/`
- `backend/tests/`

## API Contract

`GET /api/answers/{answer_id}` may return evaluation if already available, but no new evaluation-trigger endpoint is required unless needed by the existing job flow.

## Data Model Changes

Use existing `answer_evaluations` table.

## Acceptance Criteria

- [ ] Evaluation output is structured and typed.
- [ ] Scores include relevance, role depth, evidence, clarity, JD alignment, communication, and overall score.
- [ ] Feedback uses strict interviewer tone.
- [ ] Mock mode works without OpenAI API key.
- [ ] Real mode uses centralized OpenAI client and prompt registry if implemented.
- [ ] Evaluation is stored in `answer_evaluations`.
- [ ] No final report is generated in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification can use fixture transcript.

## Notes for Codex

- Do not produce vague praise.
- Do not make legal hiring claims.
- Keep scores in a consistent range.
