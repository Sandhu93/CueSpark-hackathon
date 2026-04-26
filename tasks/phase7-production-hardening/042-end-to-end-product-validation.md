# Task: End-to-End Product Validation

## Goal

Validate that CueSpark works as a complete product flow after Phase 6.

This task should not add new product features. It should test and fix the end-to-end path:

```txt
setup
-> benchmark preparation
-> benchmark dashboard
-> interview questions
-> TTS playback
-> answer submission
-> answer processing pipeline
-> agent results
-> final answer evaluation
-> readiness report generation
-> report page display
```

## Why This Task Exists

After implementing multiple backend and frontend phases, the main risk is not missing individual features. The main risk is broken integration between features.

This task confirms that the product is actually usable from start to finish.

## Scope

Validate and fix only:

- session creation
- resume/JD intake
- session preparation job
- benchmark comparison
- question listing
- TTS generation/playback
- spoken answer submission
- answer processing orchestration
- audio agent result
- benchmark gap agent result
- final answer evaluation
- report generation
- report page display
- loading/error/retry states

## Out of Scope

Do not implement:

- New AI features
- New modalities
- Authentication
- Payments
- Recruiter dashboard
- PDF export
- Email export
- Live scraping
- Major UI redesign

## Validation Scenarios

### Scenario 1 — Happy Path Spoken Interview

1. Start from `/setup`.
2. Paste a JD.
3. Paste or upload a resume.
4. Prepare the session.
5. Open match page.
6. Open benchmark dashboard.
7. Open interview room.
8. Generate/play TTS for first question.
9. Record and submit spoken answer.
10. Confirm answer is processed.
11. Confirm transcript/communication metrics appear.
12. Confirm benchmark gap result appears.
13. Confirm final answer feedback appears.
14. Generate final report.
15. Confirm report page displays correctly.

### Scenario 2 — Mock Mode Path

Run with:

```env
AI_MOCK_MODE=true
```

Confirm the full flow works without external OpenAI calls.

### Scenario 3 — Failure Recovery

Test:

- preparation failure
- TTS failure
- answer upload failure
- agent processing failure
- report missing/pending state

Each should show an actionable UI state.

## Files Likely Involved

Only modify files required to fix discovered integration issues.

Likely areas:

- `backend/app/api/`
- `backend/app/tasks/`
- `backend/app/services/`
- `frontend/src/lib/api.ts`
- `frontend/src/app/session/[sessionId]/interview/page.tsx`
- `frontend/src/app/session/[sessionId]/report/page.tsx`
- `frontend/src/components/`

## Acceptance Criteria

- [ ] Full happy path works from setup to report.
- [ ] Mock mode works end-to-end.
- [ ] Spoken answer processing produces transcript, agent results, evaluation, and report data.
- [ ] Frontend does not require manual database edits or manual job triggering.
- [ ] Failure states are understandable and recoverable.
- [ ] No new product scope is added.
- [ ] Bugs found during validation are recorded in `bugs.md` if applicable.

## Verification

Run:

```bash
docker compose up --build
pytest backend/tests
cd frontend && npm run lint && npm run build
```

Manual validation is required for the browser flow.

## Notes for Codex

- This is an integration validation task.
- Do not refactor unrelated code.
- Fix only issues that block the end-to-end product flow.
- Keep all fixes minimal and explain them clearly.
