# Task: Add Loading, Error, and Demo Polish

## Goal

Make the end-to-end demo flow understandable and resilient without expanding product scope.

## Scope

Implement only:

- Consistent loading states.
- Consistent error states.
- Empty states for missing questions/report.
- Basic retry buttons where useful.
- Demo-friendly copy and labels.
- Use fixture data only if helpful for local demo mode.

## Out of Scope

Do not implement:

- New backend features.
- Authentication.
- Payments.
- Recruiter dashboard.
- Video interview features.
- Large UI redesign.

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

- [ ] Setup, match, interview, and report pages show clear loading states.
- [ ] API errors are shown in readable form.
- [ ] Empty states explain what the user should do next.
- [ ] Demo flow can be followed without developer explanation.
- [ ] No out-of-scope features are added.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

Then manually test the complete flow.

## Notes for Codex

- This is polish, not a redesign.
- Keep changes focused and minimal.
