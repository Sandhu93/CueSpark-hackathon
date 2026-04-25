# Task: Add Benchmark-Aware Final Report Service

## Goal

Generate a strict interviewer-style final readiness report for a completed benchmark-driven interview session.

## Scope

Implement only:

- `report_generator.py` service.
- Prompt registry entry for benchmark-aware final report.
- Pydantic output schema for final report.
- Mock report generation when `AI_MOCK_MODE=true`.
- Worker task for report generation.
- Store report in `interview_reports`.
- Include benchmark comparison outputs in the report.

## Out of Scope

Do not implement:

- Frontend report page.
- PDF export.
- Emailing reports.
- Recruiter dashboard.
- Login or accounts.
- Benchmark comparison generation.

## Files Likely Involved

- `backend/app/services/report_generator.py`
- `backend/app/services/prompts.py`
- `backend/app/tasks/generate_report.py`
- `backend/app/models/`
- `backend/app/schemas/`
- `backend/tests/`

## API Contract

No public report endpoint is required unless implemented in the next task.

## Data Model Changes

Use existing `interview_reports` table.

## Report Inputs

Use available context:

- session details
- JD-resume match analysis
- benchmark comparison
- retrieved benchmark profile summaries
- interview questions
- candidate answers
- answer evaluations
- communication metrics

## Acceptance Criteria

- [ ] Final report output is structured and typed.
- [ ] Report includes readiness score and hiring recommendation.
- [ ] Report includes JD-resume match summary.
- [ ] Report includes benchmark similarity score.
- [ ] Report includes resume competitiveness score.
- [ ] Report includes evidence strength score.
- [ ] Report includes benchmark gaps and interview risk areas.
- [ ] Report includes answer-by-answer feedback summary.
- [ ] Report includes resume feedback based on benchmark gaps.
- [ ] Report includes skill gaps and preparation plan.
- [ ] Mock mode works without OpenAI API key.
- [ ] Stored report is linked to session.

## Verification

Run:

```bash
pytest backend/tests
```

## Notes for Codex

- Tone should be strict but professional.
- Do not make unsupported legal hiring claims.
- Do not claim benchmark profiles are verified hired-candidate resumes.
- The final report must make the benchmark gap visible, not hide it inside generic feedback.
