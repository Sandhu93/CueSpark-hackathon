# Task 043 — Frontend Report Page

## Goal

Build the final report page for strict interviewer feedback.

## Read First

- `docs/05-frontend-flow.md`
- `docs/06-api-contracts.md`

## Requirements

1. Create `/session/[sessionId]/report` page.
2. Trigger report generation if report does not exist.
3. Poll report job/status.
4. Show:
   - readiness score
   - hiring recommendation
   - JD-resume match summary
   - interview performance summary
   - score breakdown
   - answer-by-answer feedback
   - skill gaps
   - resume improvement suggestions
   - preparation plan

## Tone

The UI should present feedback as a strict interviewer report, not a cheerful coaching dashboard.

## Acceptance Criteria

- User can reach report after interview.
- Report data is shown in structured sections.
- Missing report/evaluations are handled gracefully.
- No login or saved history is introduced.

## Out of Scope

- PDF export.
- Sharing link.
- Email delivery.
