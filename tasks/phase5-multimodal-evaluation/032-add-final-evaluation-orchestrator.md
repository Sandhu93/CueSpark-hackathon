# Task: Add Final Evaluation Orchestrator

## Goal

Create a final evaluation orchestrator that combines modality-agent outputs into one benchmark-aware answer evaluation.

This is where CueSpark moves from separate signals to a final answer score.

## Scope

Implement only:

- `final_evaluation_orchestrator.py` service.
- Dynamic scoring based on response mode.
- Inputs from available `agent_results`.
- Typed final evaluation output.
- Store final answer evaluation in existing `answer_evaluations` or equivalent.
- Mock mode support.

## Out of Scope

Do not implement:

- Final session report.
- Frontend UI.
- PDF export.
- Email export.
- New agent analysis logic.

## Files Likely Involved

- `backend/app/services/final_evaluation_orchestrator.py`
- `backend/app/services/prompts.py` if LLM synthesis is used
- `backend/app/models/agent_result.py`
- `backend/app/models/evaluation.py`
- `backend/app/schemas/evaluation.py`
- `backend/app/tasks/evaluate_answer.py`
- `backend/tests/`

## Scoring Guidance

Scoring should change based on response mode.

### Spoken Answer

```txt
benchmark gap coverage: 30%
answer relevance: 20%
evidence/examples: 20%
communication clarity: 15%
role-specific depth: 10%
visual/audio professionalism: 5%
```

### Written Answer

```txt
relevance: 25%
structure: 20%
evidence/specificity: 20%
completeness: 15%
benchmark gap coverage: 15%
clarity: 5%
```

### Code Answer

```txt
code correctness: 35%
reasoning/explanation: 20%
complexity: 15%
edge cases: 15%
readability/testability: 10%
benchmark relevance: 5%
```

### Mixed Answer

Use a weighted blend based on which modalities are present.

## Output Schema

Recommended output:

```json
{
  "overall_score": 78,
  "category_scores": {},
  "strict_feedback": "string",
  "strengths": [],
  "weaknesses": [],
  "improvement_suggestions": [],
  "benchmark_gap_summary": "string",
  "communication_summary": "string",
  "modality_breakdown": {}
}
```

## Acceptance Criteria

- [ ] Orchestrator reads available agent results for an answer.
- [ ] Scoring changes by response mode.
- [ ] Missing optional agent results do not crash orchestration.
- [ ] Output is structured and typed.
- [ ] Final evaluation is stored.
- [ ] Feedback is strict and benchmark-aware.
- [ ] No final report generation is implemented here.

## Verification

Run:

```bash
pytest backend/tests
```

Manual check with mock agent results for spoken, written, and code answers is recommended.

## Notes for Codex

- Keep this deterministic in mock mode.
- Do not over-weight video signals.
- Benchmark gap coverage should remain central.
