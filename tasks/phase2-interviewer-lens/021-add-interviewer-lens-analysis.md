# Task: Add Interviewer Lens Analysis

## Goal

Analyze user-provided interviewer context and produce a structured interviewer lens that can later influence question generation.

## Scope

Implement only:

- `interviewer_lens_analyzer.py` service.
- Prompt registry entry for `INTERVIEWER_LENS_ANALYSIS_V1`.
- Pydantic output schema for interviewer lens analysis.
- Mock analysis when `AI_MOCK_MODE=true`.
- Optional real LLM call through centralized OpenAI client if available.
- Store analysis result on `interviewer_contexts`.

## Out of Scope

Do not implement:

- LinkedIn scraping.
- Question generation changes.
- Frontend UI.
- Report changes.
- URL crawling.
- Sensitive attribute inference.

## Files Likely Involved

- `backend/app/services/interviewer_lens_analyzer.py`
- `backend/app/services/prompts.py`
- `backend/app/schemas/interviewer_context.py`
- `backend/app/models/interviewer_context.py`
- `backend/app/tasks/analyze_interviewer_context.py`
- `backend/app/api/jobs.py`
- `backend/tests/`

## Output Requirements

The structured output should include:

```json
{
  "interviewer_name": "string | null",
  "interviewer_title": "string | null",
  "company": "string | null",
  "seniority_signal": "string | null",
  "domain_signals": [],
  "technical_focus_areas": [],
  "leadership_focus_areas": [],
  "likely_interview_style": "string",
  "likely_question_bias": [],
  "candidate_risk_from_interviewer_lens": [],
  "question_strategy": []
}
```

## Acceptance Criteria

- [ ] Analyzer returns structured Pydantic output.
- [ ] Mock mode works without OpenAI API key.
- [ ] Analysis does not claim exact prediction of questions.
- [ ] Analysis uses language like `likely focus areas`.
- [ ] Analysis does not infer sensitive attributes.
- [ ] Analysis is stored on the interviewer context row.
- [ ] No question generation changes are made.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification can use a LinkedIn-exported PDF text sample.

## Notes for Codex

- This is an interviewer-context summary, not a psychological profile.
- Do not make claims such as “the interviewer will ask.”
- Use “may focus on,” “likely to value,” and “question strategy.”
