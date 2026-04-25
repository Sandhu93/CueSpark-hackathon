# Task: Add Demo Final Readiness Report

## Goal

Build a polished mock-data final report screen that shows the intended post-interview value of CueSpark.

This is a frontend-only hackathon demo screen.

## Scope

Implement only:

- `/demo/report` route
- Readiness score
- Hiring recommendation
- JD-resume match summary
- Benchmark similarity score
- Resume competitiveness score
- Evidence strength score
- Interview risk areas
- Answer-by-answer feedback preview
- Resume improvement suggestions
- Preparation plan
- Navigation back to demo landing and real setup

## Out of Scope

Do not implement:

- Real report API
- Real evaluation API
- PDF export
- Email export
- Backend changes
- Authentication
- Payments

## Files Likely Involved

- `frontend/src/app/demo/report/page.tsx`
- `frontend/src/components/demo/`
- `frontend/src/lib/demo/mock-data.ts`

## UI Requirements

The report should show:

- Overall readiness score
- Hiring recommendation
- Benchmark similarity
- Resume competitiveness
- Evidence strength
- Strongest answer
- Weakest answer
- Top improvement priorities
- Resume bullet upgrade suggestions
- 7-day preparation plan

## Acceptance Criteria

- [ ] `/demo/report` page exists.
- [ ] Uses centralized mock data.
- [ ] Clearly labels itself as Demo Preview / Mock Data Mode.
- [ ] Shows readiness score and hiring recommendation.
- [ ] Shows benchmark-aware report sections.
- [ ] Shows answer feedback and resume improvement suggestions.
- [ ] Shows preparation plan.
- [ ] No real API calls happen.
- [ ] No unsupported hiring guarantee claims appear.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- The report should feel strict and useful, not motivational fluff.
- Keep the benchmark layer visible in the report.
