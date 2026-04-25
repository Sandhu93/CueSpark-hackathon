# Task: Add Demo Product Shell

## Goal

Make the hackathon demo feel like one cohesive CueSpark product instead of separate standalone pages.

This is a frontend-only `/demo/*` shell task.

## Scope

Implement only:

- Shared demo layout for `/demo/*`
- CueSpark demo sidebar
- Demo top bar
- Active navigation state
- Static role and benchmark-set controls
- Static demo user/avatar area
- Consistent page spacing, background, cards, and navigation

The shared shell should support these existing routes:

- `/demo`
- `/demo/benchmark`
- `/demo/interview`
- `/demo/report`

## Out of Scope

Do not implement:

- Backend changes
- Real API calls
- Authentication
- Payments
- Recruiter dashboard
- Admin screens
- Real role switching
- Real benchmark-set switching
- PDF export
- Email export
- Camera, microphone, TTS, transcription, or evaluation

## Files Likely Involved

- `frontend/src/app/demo/layout.tsx`
- `frontend/src/components/demo/`
- `frontend/src/app/demo/page.tsx`
- `frontend/src/app/demo/benchmark/page.tsx`
- `frontend/src/app/demo/interview/page.tsx`
- `frontend/src/app/demo/report/page.tsx`
- `frontend/src/lib/demo/mock-data.ts`

## UI Requirements

The demo shell should include:

1. Left sidebar
   - CueSpark brand mark/name
   - Navigation items:
     - Dashboard or Demo Home
     - Benchmark
     - Interview Room
     - Report
     - Prep Plan
     - Resources
   - Static upgrade/insights card is allowed if clearly non-functional

2. Top bar
   - Role: Senior Backend Engineer
   - Benchmark Set: Backend Engineer Set
   - Static notification/avatar controls
   - No real menus or network calls required

3. Route state
   - Current `/demo/*` page should be visually active
   - Links should only navigate to existing demo pages or safe placeholder anchors

4. Visual consistency
   - White/light SaaS product feel inspired by the provided mock images
   - Stronger product hierarchy than the current dark standalone pages
   - Keep layout responsive

## Acceptance Criteria

- [ ] `/demo/*` pages render inside a shared product shell.
- [ ] Existing `/setup` and real app routes continue to work.
- [ ] Demo shell does not call real APIs.
- [ ] Demo shell does not modify backend files.
- [ ] Navigation to `/demo`, `/demo/benchmark`, `/demo/interview`, and `/demo/report` works.
- [ ] The UI clearly remains a hackathon mock-data preview where appropriate.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- Keep this task focused on the shell and shared product feel.
- Do not redesign the benchmark, interview, or report content deeply in this task.
- Avoid unsupported claims: no hired resumes, selected profiles, emotion detection, true confidence detection, or personality scoring.
