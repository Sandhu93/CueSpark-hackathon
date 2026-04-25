# Task: Add Demo Landing and Navigation

## Goal

Add a frontend-only demo entry point that clearly explains the complete CueSpark product vision using mock data.

This must not replace the real `/setup` implementation path.

## Scope

Implement only:

- `/demo` route
- Demo intro page
- Navigation links to demo benchmark, demo interview, and demo report screens
- Clear label that this is mock-data demo mode
- CTA back to real setup flow

## Out of Scope

Do not implement:

- Backend changes
- Real session creation
- Real API calls
- Auth
- Payments
- Full redesign of existing pages

## Files Likely Involved

- `frontend/src/app/demo/page.tsx`
- `frontend/src/components/demo/`
- `frontend/src/app/page.tsx` if adding a small link to demo mode

## Page Content Requirements

The demo landing should explain:

- What CueSpark is
- Why benchmark-driven prep is different
- What the demo preview shows
- What is implemented now vs what is being previewed

Suggested copy:

```txt
This is a mock-data product preview for hackathon judging. The real backend currently supports the benchmark-preparation pipeline. This preview demonstrates the full intended experience: benchmark dashboard, interview room, and final readiness report.
```

## Acceptance Criteria

- [ ] `/demo` page exists.
- [ ] Page clearly says it is mock-data demo mode.
- [ ] Page links to `/demo/benchmark`, `/demo/interview`, and `/demo/report`.
- [ ] Page links back to real `/setup`.
- [ ] No real API calls happen from this page.
- [ ] Existing real app routes continue to work.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- Do not confuse demo mode with production-ready backend completion.
- Keep the visual style aligned with the existing app.
