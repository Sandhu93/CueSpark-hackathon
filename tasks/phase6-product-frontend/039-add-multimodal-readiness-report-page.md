# Task: Add Multimodal Readiness Report Page

## Goal

Build the production final report page that presents CueSpark's benchmark-aware multimodal readiness report to the candidate.

This page should become one of the strongest product screens. It must show not only a score, but why the candidate is or is not ready for the target role.

## Scope

Implement only:

- `/session/[sessionId]/report` route if it does not already exist.
- Generate report CTA if no report exists yet.
- Report loading/pending/failed/ready states.
- Readiness score section.
- Hiring-style recommendation without guarantee.
- JD-resume match summary.
- Benchmark similarity, resume competitiveness, and evidence strength cards.
- Benchmark gap coverage section.
- Interview risk areas.
- Answer-by-answer feedback.
- Communication summary if available.
- Visual signal summary if available.
- Written answer summary if available.
- Code answer summary if available.
- Resume improvement suggestions.
- Preparation plan.

## Out of Scope

Do not implement:

- Backend report generation logic.
- PDF export.
- Email export.
- User history dashboard.
- Recruiter dashboard.
- Payment/subscription flows.
- Demo mock UI.

## Files Likely Involved

- `frontend/src/app/session/[sessionId]/report/page.tsx`
- `frontend/src/components/report/ReadinessScoreCard.tsx`
- `frontend/src/components/report/BenchmarkGapSummary.tsx`
- `frontend/src/components/report/AnswerFeedbackList.tsx`
- `frontend/src/components/report/PreparationPlan.tsx`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/types.ts`

## UI Requirements

The page should show:

1. Header
   - target role/company if available
   - readiness score
   - hiring recommendation
   - report status

2. Benchmark readiness cards
   - JD-resume match
   - benchmark similarity
   - resume competitiveness
   - evidence strength

3. Benchmark gap coverage
   - gaps covered well
   - gaps still weak
   - interview risks

4. Answer feedback
   - question
   - answer score
   - strict feedback
   - benchmark gap coverage
   - communication/text/code highlights where available

5. Modality summaries
   - communication summary
   - visual signal summary if available
   - written answer summary if available
   - code answer summary if available

6. Resume and preparation plan
   - resume improvement suggestions
   - top improvement priorities
   - preparation plan

## Safe Language Rules

Use:

```txt
readiness recommendation
benchmark gap coverage
communication signal summary
visual signal summary
eye contact proxy
posture stability
interview risk area
```

Do not use:

```txt
emotion analysis
true confidence score
personality score
truthfulness score
selection guarantee
```

## Acceptance Criteria

- [ ] Report page route exists.
- [ ] Page reads report using the production API client.
- [ ] Page can request report generation when no report exists.
- [ ] Page handles pending, failed, and ready states.
- [ ] Page displays benchmark and multimodal report sections.
- [ ] Page avoids unsupported claims.
- [ ] No backend files are modified.
- [ ] Build succeeds.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

Manual:

1. Open `/session/{sessionId}/report`.
2. Generate report if needed.
3. Confirm readiness score, benchmark gaps, answer feedback, and modality summaries render.

## Notes for Codex

- This is a production product route, not `/demo/report`.
- The report should feel strict, useful, and benchmark-aware.
- Do not fabricate report data in the production page.
