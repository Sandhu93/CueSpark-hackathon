# Task: Polish Demo Benchmark And Report Dashboards

## Goal

Upgrade the `/demo/benchmark` and `/demo/report` screens so they look like serious benchmark-aware hiring-readiness diagnostics for hackathon judging.

This is a frontend-only `/demo/*` visual and information-design task.

## Scope

Implement only:

- Visual polish for `/demo/benchmark`
- Visual polish for `/demo/report`
- Dashboard-style score cards
- Chart-like static visuals using existing mock data
- Better risk labels, evidence sections, and recommendation hierarchy
- Stronger benchmark narrative across both pages

## Out of Scope

Do not implement:

- Backend changes
- Real API calls
- Real benchmark computation
- Real report generation
- PDF export
- Email export
- Authentication
- Payments
- Recruiter dashboard
- Scraping
- Hired-resume or selected-profile claims

## Files Likely Involved

- `frontend/src/app/demo/benchmark/page.tsx`
- `frontend/src/app/demo/report/page.tsx`
- `frontend/src/components/demo/`
- `frontend/src/lib/demo/mock-data.ts`
- `frontend/src/lib/demo/types.ts`

## UI Requirements

### `/demo/benchmark`

Make the page feel closer to a benchmark gap dashboard:

- Main title: `CueSpark Benchmark Gap Dashboard`
- Role and benchmark-set context should be visible from the shared shell or page header.
- Score cards:
  - Benchmark Similarity
  - Resume Competitiveness
  - Evidence Strength
  - Hiring Bar Gap
- Add static chart-like visuals where useful:
  - mini trend lines
  - progress bars
  - radar/bar-style benchmark coverage
  - evidence distribution
- Show:
  - top benchmark gaps
  - benchmark profile match summary
  - generated question targets
  - actionable recommendations
  - interview strategy chips

### `/demo/report`

Make the page feel closer to a final benchmark-aware readiness report:

- Main title: `Final Benchmark-Aware Readiness Report`
- Cards:
  - Readiness Score
  - Benchmark Similarity
  - Evidence Strength
  - Hiring Recommendation
- Add static chart-like visuals where useful:
  - score gauge
  - gap summary bars
  - answer performance rows
  - evidence distribution
- Show:
  - interview risk areas
  - evidence upgrade suggestions
  - resume rewrite priorities
  - preparation plan

## Data Requirements

- Use centralized mock data from `frontend/src/lib/demo/mock-data.ts`.
- If additional demo values are needed for chart-like visuals, add them to centralized mock data/types.
- Do not hardcode main report or benchmark data directly inside page components.

## Acceptance Criteria

- [ ] `/demo/benchmark` looks like a polished dashboard, not a text-heavy page.
- [ ] `/demo/report` looks like a final diagnostic report, not a plain summary page.
- [ ] Both pages keep the benchmark layer visible throughout.
- [ ] Both pages use centralized mock data.
- [ ] No real API calls happen.
- [ ] No backend files are modified.
- [ ] No unsupported claims appear.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- Keep wording strict and useful, not motivational.
- Use safe wording: benchmark profiles, role benchmark corpus, curated top-candidate archetypes, evidence gaps, hiring bar gap, question targets.
- Avoid claims about hired resumes, selected profiles, true confidence detection, emotion detection, or personality scoring.
