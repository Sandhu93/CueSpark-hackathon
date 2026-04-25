# Task: Add Benchmark Gap Coverage Agent

## Goal

Add a benchmark-gap coverage agent that evaluates whether a candidate response directly addresses the benchmark gap that the question was designed to test.

This is the core CueSpark differentiator inside the multimodal evaluation pipeline.

## Scope

Implement only:

- `benchmark_gap_agent.py` service.
- Prompt registry entry for benchmark gap coverage analysis.
- Pydantic output schema.
- Mock mode output when `AI_MOCK_MODE=true`.
- Store agent output in `agent_results`.

## Out of Scope

Do not implement:

- Audio transcription.
- Text/code/video analysis.
- Final score orchestration.
- Final report.
- Frontend UI.

## Files Likely Involved

- `backend/app/services/benchmark_gap_agent.py`
- `backend/app/services/prompts.py`
- `backend/app/schemas/agent_results.py`
- `backend/app/models/agent_result.py`
- `backend/app/tasks/analyze_benchmark_gap_coverage.py`
- `backend/tests/`

## Input

Use:

- question text
- benchmark gap references
- expected signal
- transcript, text answer, or code explanation
- existing modality-agent summaries if available
- JD/resume/benchmark comparison context if available

## Output Schema

Recommended output:

```json
{
  "benchmark_gap_coverage_score": 6,
  "covered_gaps": [],
  "missed_gaps": [],
  "evidence_quality": "weak | moderate | strong",
  "gap_specific_feedback": "string",
  "remaining_interview_risk": "string"
}
```

## Acceptance Criteria

- [ ] Benchmark gap agent exists.
- [ ] Output is structured and typed.
- [ ] Mock mode works without OpenAI API key.
- [ ] Agent uses benchmark gap references from the question where available.
- [ ] Agent output is stored in `agent_results`.
- [ ] No final score/report is generated here.

## Verification

Run:

```bash
pytest backend/tests
```

Manual check with a benchmark-gap-driven question and sample answer is acceptable.

## Notes for Codex

- This should be stricter than generic answer evaluation.
- The key question is: did the response prove the gap that CueSpark identified?
