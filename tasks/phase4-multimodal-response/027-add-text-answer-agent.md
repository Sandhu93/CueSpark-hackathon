# Task: Add Text Answer Agent

## Goal

Add a text-answer analysis agent for written responses, pseudocode, case-study answers, stakeholder communication answers, and non-technical written interview tasks.

This agent evaluates the quality of the written answer, not the candidate's personality or intent.

## Scope

Implement only:

- `text_answer_agent.py` service.
- Prompt registry entry for text answer analysis.
- Pydantic output schema for text answer analysis.
- Mock mode output when `AI_MOCK_MODE=true`.
- Worker task or service call to analyze text answers.
- Store structured text analysis result in a reusable agent result store or answer metadata.

## Out of Scope

Do not implement:

- Code analysis.
- Audio transcription.
- Video analysis.
- Final score orchestration.
- Final report.
- Frontend rich text editor.

## Files Likely Involved

- `backend/app/services/text_answer_agent.py`
- `backend/app/services/prompts.py`
- `backend/app/schemas/agent_results.py`
- `backend/app/models/answer.py`
- `backend/app/tasks/analyze_text_answer.py`
- `backend/tests/`

## Input

Use:

- question text
- expected signal
- benchmark gap references
- written answer text
- JD/resume context if easily available

## Output Schema

Recommended output:

```json
{
  "relevance_score": 8,
  "structure_score": 7,
  "specificity_score": 6,
  "evidence_score": 5,
  "clarity_score": 8,
  "completeness_score": 7,
  "strengths": [],
  "weaknesses": [],
  "improvement_suggestions": []
}
```

## Acceptance Criteria

- [ ] Text answer agent exists.
- [ ] Output is structured and typed.
- [ ] Mock mode works without OpenAI API key.
- [ ] Written answer can be analyzed independently of audio.
- [ ] Agent uses benchmark gap references when available.
- [ ] No final scoring/reporting is implemented here.

## Verification

Run:

```bash
pytest backend/tests
```

Manual check with a written answer fixture is acceptable.

## Notes for Codex

- Keep this focused on written answer quality.
- Avoid generic motivational feedback.
- Do not score personality or emotions.
