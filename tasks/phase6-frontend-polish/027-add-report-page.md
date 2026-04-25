# Task: Add Benchmark-Aware Final Report Page

## Goal

Build the frontend report page that displays the strict interviewer-style final readiness report, including benchmark comparison and evidence-gap findings.

## Scope

Implement only:

- `/session/[sessionId]/report` page.
- Trigger report generation if no report exists and user requests it.
- Fetch report status/result.
- Display readiness score.
- Display hiring recommendation.
- Display JD-resume match summary.
- Display benchmark similarity score.
- Display resume competitiveness score.
- Display evidence strength score.
- Display benchmark gaps and interview risk areas.
- Display skill gaps, answer feedback, resume feedback, and improvement plan.
- Loading and error states.

## Out of Scope

Do not implement:

- PDF export.
- Email report.
- Login.
- Recruiter dashboard.
- Payment/subscription gate.
- Live scraping UI.
- Claims that benchmark profiles are verified selected/hired resumes.

## Files Likely Involved

- `frontend/src/app/session/[sessionId]/report/page.tsx`
- `frontend/src/components/`
- `frontend/src/lib/api.ts`

## API Contract

Use:

- `POST /api/sessions/{session_id}/report`
- `GET /api/sessions/{session_id}/report`

## Data Model Changes

None.

## Acceptance Criteria

- [ ] Report page loads by session ID.
- [ ] User can trigger report generation if report is missing.
- [ ] Report page displays readiness score and recommendation.
- [ ] Report page displays benchmark similarity, resume competitiveness, and evidence strength scores when available.
- [ ] Report page displays benchmark gaps and interview risk areas.
- [ ] Report page displays major answer feedback sections.
- [ ] Report page displays resume improvement suggestions based on benchmark gaps.
- [ ] Missing/pending report state is handled.
- [ ] No PDF/email/export feature is added.
- [ ] No unsupported confidence, emotion, or hired-resume claims are shown.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

Manual browser verification is recommended.

## Notes for Codex

- Keep tone and labels aligned with strict interviewer style.
- Avoid unsupported claims like true confidence or personality detection.
- The report must make the benchmark layer visible; do not reduce it to generic feedback.
