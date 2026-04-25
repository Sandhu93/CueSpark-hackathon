# Task: Add Code Evaluation Agent

## Goal

Add a code evaluation agent for coding interview questions and technical implementation tasks.

The first version should focus on safe static review and structured evaluation. Do not execute arbitrary candidate code on the main backend.

## Scope

Implement only:

- `code_evaluation_agent.py` service.
- Prompt registry entry for code evaluation.
- Pydantic output schema for code evaluation.
- Mock mode output when `AI_MOCK_MODE=true`.
- Static LLM-based/code-review-based evaluation.
- Optional support for provided sample test cases as text, without executing code.
- Store structured code analysis result in reusable agent result store or answer metadata.

## Out of Scope

Do not implement:

- Arbitrary code execution.
- Online judge sandbox.
- Dockerized runtime execution.
- Monaco editor frontend.
- Final score orchestration.
- Final report.
- Video analysis.

## Files Likely Involved

- `backend/app/services/code_evaluation_agent.py`
- `backend/app/services/prompts.py`
- `backend/app/schemas/agent_results.py`
- `backend/app/models/answer.py`
- `backend/app/tasks/analyze_code_answer.py`
- `backend/tests/`

## Input

Use:

- question text
- problem statement
- expected signal
- code answer
- code language
- candidate explanation if available
- benchmark gap references if available

## Output Schema

Recommended output:

```json
{
  "correctness_score": 7,
  "edge_case_score": 6,
  "complexity_score": 8,
  "readability_score": 7,
  "testability_score": 6,
  "explanation_score": 7,
  "strengths": [],
  "weaknesses": [],
  "suggested_improvements": [],
  "complexity_analysis": "string"
}
```

## Acceptance Criteria

- [ ] Code evaluation agent exists.
- [ ] Output is structured and typed.
- [ ] Mock mode works without OpenAI API key.
- [ ] Agent does not execute arbitrary code.
- [ ] Agent evaluates correctness, edge cases, complexity, readability, testability, and explanation quality.
- [ ] No final scoring/reporting is implemented here.

## Verification

Run:

```bash
pytest backend/tests
```

Manual check with a simple code answer fixture is acceptable.

## Notes for Codex

- Do not run candidate code directly.
- Future code execution must use a sandboxed worker/runtime.
- This task is static analysis only.
