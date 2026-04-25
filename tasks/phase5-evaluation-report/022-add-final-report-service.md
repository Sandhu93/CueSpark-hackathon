# Task: Add Final Report Service

## Goal

Generate a strict interviewer-style final readiness report for a completed interview session.

## Scope

Implement only:

- `report_generator.py` service.
- Prompt registry entry for final report.
- Pydantic output schema for final report.
- Mock report generation when `AI_MOCK_MODE=true`.
- Worker task for report generation.
- Store report in `interview_reports`.

## Out of Scope

Do not implement:

- Frontend report page.
- PDF export.
- Emailing reports.
- Recruiter dashboard.
- Login or accounts.

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

## Acceptance Criteria

- [ ] Final report output is structured and typed.
- [ ] Report includes readiness score and hiring recommendation.
- [ ] Report includes JD-resume match summary.
- [ ] Report includes answer-by-answer feedback summary.
- [ ] Report includes skill gaps, resume feedback, and preparation plan.
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
