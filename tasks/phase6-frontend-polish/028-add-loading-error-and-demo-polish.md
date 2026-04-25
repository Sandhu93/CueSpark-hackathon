# Task: Add Loading, Error, and Demo Polish

## Goal

Make the end-to-end benchmark-driven demo flow understandable and resilient without expanding product scope.

The demo should clearly communicate that CueSpark compares the candidate against curated benchmark profiles and generates the interview from benchmark gaps.

## Scope

Implement only:

- Consistent loading states.
- Consistent error states.
- Empty states for missing match data, benchmark data, questions, answers, and report.
- Basic retry buttons where useful.
- Demo-friendly copy and labels.
- Benchmark explanation copy for judges/users.
- Use fixture data only if helpful for local demo mode.

## Out of Scope

Do not implement:

- New backend features.
- Authentication.
- Payments.
- Recruiter dashboard.
- Video interview features.
- Large UI redesign.
- Live scraping UI.
- Claims that benchmark profiles are verified hired/selected resumes.

## Files Likely Involved

- `frontend/src/app/`
- `frontend/src/components/`
- `frontend/src/lib/api.ts`
- `README.md`

## API Contract

No new API endpoint is required in this task.

## Data Model Changes

None.

## Acceptance Criteria

- [ ] Setup, match, benchmark, interview, and report pages show clear loading states.
- [ ] API errors are shown in readable form.
- [ ] Empty states explain what the user should do next.
- [ ] Benchmark dashboard explains the benchmark corpus honestly.
- [ ] Demo flow can be followed without developer explanation.
- [ ] Copy reinforces the core message: practice against the hiring bar, not just an AI chatbot.
- [ ] No unsupported claims about confidence, emotions, hired resumes, or selected profiles are shown.
- [ ] No out-of-scope features are added.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

Then manually test the complete flow:

```txt
setup -> match -> benchmark -> interview -> report
```

## Notes for Codex

- This is polish, not a redesign.
- Keep changes focused and minimal.
- The benchmark dashboard should remain the most obvious novelty moment.
