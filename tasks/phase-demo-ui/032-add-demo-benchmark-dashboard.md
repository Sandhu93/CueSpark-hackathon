# Task: Add Demo Benchmark Dashboard

## Goal

Build a polished mock-data benchmark dashboard that shows the core novelty of CueSpark for hackathon judges.

This screen should communicate the product differentiation within 10 seconds.

## Scope

Implement only:

- `/demo/benchmark` route
- Benchmark score cards
- Hiring bar gap section
- Missing skills section
- Weak evidence section
- Missing metrics section
- Weak ownership signals section
- Interview risk areas section
- Question targets section
- Navigation to demo interview room

## Out of Scope

Do not implement:

- Real API calls
- Backend changes
- Real session data
- Real benchmark computation
- Interview recording
- Report generation

## Files Likely Involved

- `frontend/src/app/demo/benchmark/page.tsx`
- `frontend/src/components/demo/`
- `frontend/src/lib/demo/mock-data.ts`

## UI Requirements

The page should include:

```txt
Candidate vs Hiring Benchmark
```

Main scores:

- Benchmark Similarity
- Resume Competitiveness
- Evidence Strength
- Hiring Bar Gap

Gap sections:

- Missing skills
- Weak evidence
- Missing metrics
- Weak ownership signals
- Interview risk areas
- Recommended resume fixes
- Question targets

## Acceptance Criteria

- [ ] `/demo/benchmark` page exists.
- [ ] Uses centralized mock data.
- [ ] Clearly labels itself as Demo Preview / Mock Data Mode.
- [ ] Shows benchmark similarity, competitiveness, evidence strength, and hiring bar gap.
- [ ] Shows gaps and risk areas in a clear visual layout.
- [ ] Has CTA to `/demo/interview`.
- [ ] No real API calls happen.
- [ ] No unsupported claims about hired resumes or selected profiles appear.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- This is the most important judge-facing demo screen.
- Keep the copy sharp: benchmark-driven, evidence gaps, hiring bar.
