# Task: Add Benchmark-Aware Answer Evaluation Service

## Goal

Evaluate each candidate answer using the question, expected signal, JD/resume context, benchmark gap being tested, transcript, and communication metrics.

## Scope

Implement only:

- `answer_evaluator.py` service.
- Prompt registry entry for benchmark-aware answer evaluation.
- Pydantic output schema for evaluation.
- Mock evaluation when `AI_MOCK_MODE=true`.
- Worker task for evaluating an answer.
- Store results in `answer_evaluations`.
- Include benchmark gap coverage scoring when the question is tied to benchmark gaps.

## Out of Scope

Do not implement:

- Final report generation.
- Adaptive follow-ups.
- Frontend report UI.
- Video analysis.
- Benchmark comparison generation.

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

## Evaluation Context

Use available context:

- question text
- expected signal
- question category
- question source/provenance
- benchmark gap references, if available
- JD context
- resume context
- benchmark comparison context, if available
- answer transcript
- communication metrics

## Acceptance Criteria

- [ ] Evaluation output is structured and typed.
- [ ] Scores include relevance, role depth, evidence, clarity, JD alignment, benchmark gap coverage, communication, and overall score.
- [ ] Feedback uses strict interviewer tone.
- [ ] Feedback explicitly states whether the answer addressed the benchmark gap when applicable.
- [ ] Mock mode works without OpenAI API key.
- [ ] Real mode uses centralized OpenAI client and prompt registry if implemented.
- [ ] Evaluation is stored in `answer_evaluations`.
- [ ] No final report is generated in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification can use fixture transcript and a benchmark-gap-driven question.

## Notes for Codex

- Do not produce vague praise.
- Do not make legal hiring claims.
- Keep scores in a consistent range.
- Do not claim the candidate is confident; use communication signals only.
